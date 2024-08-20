from collections.abc import Iterable
from inspect import signature
from typing import List

from pydantic import BaseModel

from app.profile_enricher.profiler import Profiler
from app.profile_enricher.types import ValidationRecommendation
from app.xapi_converter.transformer import *
from enums import (
    CustomTraceFormatModelEnum,
    CustomTraceFormatOutputMappingEnum,
    CustomTraceFormatStrEnum,
)
from trace_formats.enums import TraceFormatEnum
from trace_formats.models.mapping_config import (
    CompleteConfigModel,
    MainMappingModel,
    OutputMappingModel, ConditionOutputMappingModel,
)
from utils.utils_dict import (
    convert_yaml_file_to_json,
    get_value_from_flat_key,
    set_value_from_flat_key,
)


# TODO: Revoir l'architecture de la classe
# TODO: Documenter et test unitaire du code


# TODO: Move?
class FinalMappingModel(BaseModel):
    output_field: str | None
    value: Any


DEFAULT_CONDITION = "default"


def get_config_model_from_yaml_file(file_path: str) -> CompleteConfigModel:
    """From a file path (for a YAML file) get the CompleteConfigModel used for the mapping process

    Args:
        file_path (str): YAML file path

    Returns:
        CompleteConfigModel: Model used to map input trace
    """
    json_config = convert_yaml_file_to_json(file_path)
    # Load mapping in Model
    return CompleteConfigModel(**json_config)


def get_mapping_by_input_and_output_format(
    input_format: str | TraceFormatEnum, output_format: str | TraceFormatEnum
) -> CompleteConfigModel:
    """From the input_format and the output_format, retrieve the correct mapping config (if exists)

    Args:
        input_format (str | TraceFormatEnum): Trace input format
        output_format (str | TraceFormatEnum): Trace output format

    Raises:
        ValueError: No mapping for this output format found.
        ValueError: No mapping from this input to this output format found.
        ValueError: Mapping unloadable (empty file, wrong path...)

    Returns:
        CompleteConfigModel: Mapping config model
    """
    # Get correct mapping enum
    mapping_config = None
    try:
        if isinstance(output_format, str):
            enum_key = CustomTraceFormatStrEnum(output_format).name
            mappings = CustomTraceFormatOutputMappingEnum[enum_key].value
        elif isinstance(output_format, TraceFormatEnum):
            mappings = CustomTraceFormatOutputMappingEnum[output_format.name].value
    except (ValueError, KeyError) as e:
        raise ValueError(f"Output mapping enum to {output_format} not found")

    try:
        if isinstance(input_format, str):
            enum_key = CustomTraceFormatStrEnum(input_format).name
            mapping_config = mappings[enum_key]
        elif isinstance(input_format, TraceFormatEnum):
            mapping_config = mappings[input_format.name]
    except (ValueError, KeyError) as e:
        raise ValueError(f"Mapping from {input_format} to {output_format} not found")

    # Read config file
    if isinstance(mapping_config, TraceFormatEnum):
        return get_config_model_from_yaml_file(mapping_config.value)
    else:
        raise ValueError("Could not load mapping config into model")


class MappingInput:
    """This class handles mapping from an input format to an output format, using a config model.

    It will not automatically detect the input format from the input trace. An explicit specification is needed.
    """

    def __init__(
        self,
        input_format: CustomTraceFormatModelEnum,
        mapping_to_apply: CompleteConfigModel,
        output_format: CustomTraceFormatModelEnum,  # = TraceFormatModelEnum.XAPI,
        profile_enricher: Profiler
    ) -> None:
        self.input_format = input_format
        self.output_format = output_format
        self.mapping_to_apply = mapping_to_apply
        self.profile_enricher = profile_enricher
        self.profile = None

    def transformation_custom(
        self,
        custom_input: List[str],
        arguments: Iterable[Any] | None = None,
        deploy_arguments: bool = True,
    ) -> Any:
        if custom_input:
            # Gérer erreur ici (lors de l'application de eval) + Gérer l'erreur en cas de fonction non callable
            custom_code = eval(custom_input[0])
            nb_arguments = len(signature(custom_code).parameters)
            response = (
                custom_code(*arguments)
                if deploy_arguments or nb_arguments > 1
                else custom_code(arguments)
            )
            return self.transformation_custom(
                custom_input[1:], arguments=response, deploy_arguments=False
            )
        return arguments

    def transformation_value(
        self, value: Any, arguments: list[Any] | None = None
    ) -> Any:
        if not arguments:
            arguments = list()
        return value

    # TODO: > OK for 1 output, but not multiple, return list?
    def transformation_switch(
        self, switch_value: List[ConditionOutputMappingModel], arguments: list[Any] | None = None
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
        list_response = []
        # Check each condition
        for condition in switch_value:
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
        transformation_model: OutputMappingModel,
        output_field: str | None,
        arguments: list[Any] | None = None,
    ) -> list[FinalMappingModel]:
        if not arguments:
            arguments = list()
        if transformation_model.custom:
            value = self.transformation_custom(transformation_model.custom, arguments)
        elif transformation_model.value:
            value = self.transformation_value(transformation_model.value, arguments)
        elif transformation_model.switch:
            return self.transformation_switch(transformation_model.switch, arguments)
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

        if basic_output.profile:
            self.profile = basic_output.profile

        # Single output
        if basic_output.custom or basic_output.value or basic_output.switch:
            # value = launch_transformation(basic_output.transformation, basic_output.output_field, arguments)
            # list_response.append(
            #     FinalMappingModel(output_field=basic_output.output_field, value=value)
            # )
            list_response.extend(
                self.launch_transformation(
                    basic_output, basic_output.output_field, arguments
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
        output_trace = remove_empty_elements(output_trace)
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

    def mapping(self, input_trace):
        # Mapping
        # TODO: Sortir ce bloc de mapping
        # TODO: Regarder pour donner la possibilité de faire de mapping sans forcément être dans l'Enum
        # TODO: Isoler les parties mapping/enums...
        output_trace = {}
        output_trace = self.handle_mapping(
            self.mapping_to_apply.mappings, input_trace, output_trace
        )
        # Default
        output_trace = self.handle_default(self.mapping_to_apply.default_values, output_trace)

        # Return response
        return output_trace

    def _enrich_with_profile(self, output_trace: dict):
        """
        Enrich trace with profile
        """
        self.profile_enricher.enrich_trace(profile=self.profile, trace=output_trace)

    def _validate_with_profile(self, output_trace: dict):
        """
        Validate trace with profile
        """
        errors = self.profile_enricher.validate_trace(
            profile=self.profile,
            trace=output_trace,
        )
        if errors:
            raise ValueError(f"The trace does not match the profile: {errors}")

    def get_recommendations(self, output_trace: dict) -> list[ValidationRecommendation]:
        """
        Get recommendations to improve the trace
        """
        if not self.profile:
            return []

        return self.profile_enricher.get_recommendations(
            profile=self.profile,
            trace=output_trace,
        )

    def run(self, input_trace: dict) -> dict:
        ##### MAIN FUNCTION #####
        if not self.input_format or not self.output_format or not self.mapping_to_apply:
            raise ValueError(
                "'input_format', 'output_format' or 'mapping_to_apply' cannot be empty"
            )

        # Check if input_trace match input_format (model validation)
        # An exception will be raised of not correct model
        self.input_format.value(**input_trace)  # TODO: To test

        output_trace = self.mapping(input_trace)

        # Output format (always xAPI non?)
        # An exception will be raised of not correct model
        self.output_format.value(**output_trace)  # TODO: To test

        if self.profile is not None:
            self._enrich_with_profile(output_trace=output_trace)
            self._validate_with_profile(output_trace=output_trace)

        # Check if output_trace match output_format (model validation)
        return output_trace
