from collections.abc import Iterable
from inspect import signature
from typing import Any

import yaml
from enums import TraceFormatEnum, TraceFormatMappingEnum, TraceFormatModelEnum
from models.mapping_config import (
    BasicTransformationModel,
    CompleteConfigModel,
    CustomTransformationModel,
    MainMappingModel,
    OutputMappingModel,
    SwitchTransformationModel,
    ValueTransformationModel,
)
from pydantic import BaseModel
from utils.utils_dict import get_value_from_flat_key, set_value_from_flat_key

from app.xapi_converter.transformer import *

# TODO: Revoir l'architecture de la classe
# TODO: Documenter et test unitaire du code


# TODO: Move?
class FinalMappingModel(BaseModel):
    output_field: str | None
    value: Any


DEFAULT_CONDITION = "default"


def get_mapping_by_trace_format(trace_format: str | TraceFormatEnum) -> CompleteConfigModel:
    # Get correct Key
    try:
        if isinstance(trace_format, str):
            trace_format = TraceFormatMappingEnum[trace_format]
        elif isinstance(trace_format, TraceFormatEnum):
            trace_format = TraceFormatMappingEnum[trace_format.name]
    except (ValueError, KeyError) as e:
        raise ValueError(f"{trace_format} not found")

    # Read config file
    if isinstance(trace_format, TraceFormatMappingEnum):
        json_config = convert_yaml_file_to_json(trace_format.value)
        # Load mapping in Model
        return CompleteConfigModel(**json_config)
    else:
        raise ValueError("Could not load mapping config into model")


def convert_yaml_file_to_json(yaml_path: str) -> dict:
    if yaml_path:
        with open(yaml_path, "r") as file:
            return yaml.safe_load(file)
    else:
        raise ValueError("'yaml_path' cannot be empty")


class MappingInput:
    """This class handles mapping from an input format to an output format, using a config model.

    It will not automatically detect the input format from the input trace. An explicit specification is needed.
    """

    def __init__(
        self,
        input_format: TraceFormatModelEnum,
        mapping_to_apply: CompleteConfigModel,
        output_format: TraceFormatModelEnum,  # = TraceFormatModelEnum.XAPI,
    ) -> None:
        self.input_format = input_format
        self.output_format = output_format
        self.mapping_to_apply = mapping_to_apply

    def transformation_custom(
        self,
        custom_input: CustomTransformationModel | list[str],
        arguments: Iterable[Any] | None = None,
        deploy_arguments: bool = True,
    ) -> Any:
        if not arguments:
            arguments = list()
        if isinstance(custom_input, CustomTransformationModel):
            custom_input = custom_input.custom

        if custom_input:
            # Gérer erreur ici (lors de l'application de eval) + Gérer l'erreur en cas de fonction non callable
            custom_code = eval(custom_input.pop(0))
            nb_arguments = len(signature(custom_code).parameters)
            response = (
                custom_code(*arguments)
                if deploy_arguments or nb_arguments > 1
                else custom_code(arguments)
            )
            return self.transformation_custom(
                custom_input, arguments=response, deploy_arguments=False
            )
        return arguments

    # CUSTOM TESTING
    # test = CustomTransformationModel(custom=["lambda a, b: (a+b, a-b)", "lambda a: a+b"])
    # # test = CustomTransformationModel(custom=["lambda a, b: a + b"])
    # print(transformation_custom(test, 2, 3))

    def transformation_value(
        self, value: ValueTransformationModel, arguments: list[Any] | None = None
    ) -> Any:
        if not arguments:
            arguments = list()
        return value.value

    # TODO: > OK for 1 output, but not multiple, return list?
    def transformation_switch(
        self, switch_value: SwitchTransformationModel, arguments: list[Any] | None = None
    ) -> list[FinalMappingModel]:
        # def action(condition: ConditionOutputMappingModel):
        #     list_response = []
        #     # Single output
        #     if condition.transformation:
        #         value = launch_transformation(condition.transformation, *args, **kwargs)
        #         return list_response.append(SwitchTransformerResponse(output_field=condition.output_field, value=value))
        #     # Multiple output
        #     elif condition.multiple:
        #         for each_output in condition.multiple:
        #             # GO
        #     else:
        #         return list_response.append(SwitchTransformerResponse(output_field=condition.output_field, value=None))
        # TODO: recheck this part
        if not arguments:
            arguments = list()
        list_condition = switch_value.switch
        list_response = []
        # Check each condition
        for condition in list_condition:
            if str(condition.condition).lower().strip() != DEFAULT_CONDITION:
                lambda_condition = eval(condition.condition)
                try:
                    if lambda_condition(*arguments):
                        list_response.extend(self.handle_output(condition, arguments))
                        return list_response
                except TypeError as e:
                    print("Condition unvalid")
            else:
                list_response.extend(self.handle_output(condition, arguments))
                return list_response
        list_response.append(FinalMappingModel(output_field=None, value=None))
        return list_response

    def launch_transformation(
        self,
        transformation_model: BasicTransformationModel,
        output_field: str | None,
        arguments: list[Any] | None = None,
    ) -> list[FinalMappingModel]:
        if not arguments:
            arguments = list()
        if isinstance(transformation_model, CustomTransformationModel):
            value = self.transformation_custom(transformation_model, arguments)
        elif isinstance(transformation_model, ValueTransformationModel):
            value = self.transformation_value(transformation_model, arguments)
        elif isinstance(transformation_model, SwitchTransformationModel):
            return self.transformation_switch(transformation_model, arguments)
        else:
            raise TypeError(f"Unknow transformation model: {type(transformation_model)}")
        return [FinalMappingModel(output_field=output_field, value=value)]

    def handle_output(
        self, basic_output: OutputMappingModel, arguments: list[Any] | None = None
    ) -> list[FinalMappingModel]:
        if not arguments:
            arguments = list()
        # TODO: Check code here... append models?
        list_response = []

        # Single output
        if basic_output.transformation:
            # value = launch_transformation(basic_output.transformation, basic_output.output_field, arguments)
            # list_response.append(
            #     FinalMappingModel(output_field=basic_output.output_field, value=value)
            # )
            list_response.extend(
                self.launch_transformation(
                    basic_output.transformation, basic_output.output_field, arguments
                )
            )
        # Multiple output
        elif basic_output.multiple:
            for each_output in basic_output.multiple:
                list_response.extend(self.handle_output(each_output, arguments))
        else:
            value = arguments[0] if arguments else None
            list_response.append(
                FinalMappingModel(output_field=basic_output.output_field, value=value)
            )
        return list_response

    """
        C'est pas None forcément, faut voir pour le retour des valeurs en mapping direct
        (sans transformation), faire attention, ici il y a des tuples
    """

    def handle_mapping(
        self,
        full_mapping_content: list[MainMappingModel],
        input_trace: dict,
        output_trace: dict | None = None,
    ) -> dict:
        if not output_trace:
            output_trace = {}
        for mapping_content in full_mapping_content:
            # I have the input key
            list_input_key = mapping_content.input_fields
            # Get input values
            list_input_value = [
                get_value_from_flat_key(input_trace, input_key) for input_key in list_input_key
            ]
            # Get simplified outputs
            output_trace = self.build_trace_with_output(
                mapping_content.output_fields,
                output_trace,
                True,
                list_input_value,
            )  # C'EST HYPER MAL GERE LES TRUCS DE ARGS ET KWARGS, PASSER PLUTÖT VIA DES VARIABLES FIXE, C'EST MIEUX NON? A CREUSER, MAIS LA C4EST TERRIBLE
        return output_trace
        # list_simplified_outputs = handle_output(mapping_content.output_fields, *list_inputs)
        # for simplified_outputs in list_simplified_outputs:
        #     if simplified_outputs.output_field:
        #         trace = set_value_from_flat_key(
        #             trace, simplified_outputs.output_field, simplified_outputs.value
        #         )

    def handle_default(
        self, full_default_content: list[OutputMappingModel], output_trace: dict | None = None
    ) -> dict:
        if not output_trace:
            output_trace = {}
        for default_content in full_default_content:
            output_trace = self.build_trace_with_output(
                default_content, output_trace, overwrite=False
            )
        return output_trace

    def build_trace_with_output(
        self,
        output_content: OutputMappingModel,
        output_trace: dict | None = None,
        overwrite: bool = True,
        arguments: list[Any] | None = None,
    ) -> dict:
        if not output_trace:
            output_trace = {}
        if not arguments:
            arguments = list()
        list_simplified_outputs = self.handle_output(output_content, arguments)
        for simplified_outputs in list_simplified_outputs:
            if simplified_outputs.output_field:
                output_trace = set_value_from_flat_key(
                    output_trace,
                    simplified_outputs.output_field,
                    simplified_outputs.value,
                    overwrite=overwrite,
                )
        return output_trace

    # def refactor_complete_config():
    # Ajouter les outputs partout où il faut
    # Transformation : "bob" par défaut c'est transformation: value: "bob", faire/mettre en place la prise en compte.

    def run(self, input_trace: dict) -> dict:
        ##### MAIN FUNCTION #####
        if not self.input_format or not self.output_format or not self.mapping_to_apply:
            raise ValueError(
                "'input_format', 'output_format' or 'mapping_to_apply' cannot be empty"
            )

        # Check if input_trace match input_format (model validation)
        # An exception will be raised of not correct model
        self.input_format.value(**input_trace)  # TODO: To test

        # Mapping
        output_trace = {}
        output_trace = self.handle_mapping(
            self.mapping_to_apply.mappings, input_trace, output_trace
        )
        # Default
        output_trace = self.handle_default(self.mapping_to_apply.default_values, output_trace)

        # Output format (always xAPI non?)
        # An exception will be raised of not correct model
        self.output_format.value(**output_trace)  # TODO: To test
        # Check if output_trace match output_format (model validation)
        return output_trace
