from typing import Any, Callable

from extensions.enums import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum
from pydantic import ValidationError
from type.types import JsonType
from utils.utils_dict import (get_value_from_flat_key, remove_empty_elements,
                              set_value_from_flat_key)

from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract

# This import is used for the eval method :
from .available_functions.mapping_runnable_functions import *
from .exceptions import (CodeEvaluationException, InputTraceToModelException,
                         MapperException, OutputTraceToModelException)
from .models.mapping_models import FinalMappingModel
from .models.mapping_schema import (ConditionOutputMappingModel, MappingSchema,
                                    OutputMappingModel)

DEFAULT_CONDITION = "default"


class MappingEngine:
    """
    Handles mapping from an input format to an output format using a config model.
    """

    def __init__(
        self,
        input_format: CustomTraceFormatModelEnum,
        mapping_to_apply: MappingSchema,
        output_format: CustomTraceFormatModelEnum,
        logger: LoggerContract,
    ):
        """
        Initialize the MappingEngine.

        :param input_format: The input format of the trace
        :param mapping_to_apply: The mapping configuration to apply
        :param output_format: The desired output format
        :param logger: LoggerContract implementation for logging
        """
        self.input_format = input_format
        self.output_format = output_format
        self.mapping_to_apply = mapping_to_apply
        self.logger = logger
        self.log_context = {
            "input_format": self.input_format.name,
            "output_format": self.output_format.name,
        }
        self.profile = None

    def run(self, input_trace: Trace) -> Trace:
        """
        Main function : run the mapping process on the input trace.

        :param input_trace: The input trace to map
        :return: The mapped output trace
        """
        self._validate_inputs(input_trace=input_trace)
        mapped_data = self._apply_mapping(input_data=input_trace.data)
        output_data = self._post_process(mapped_data=mapped_data)
        return self._create_output_trace(output_data=output_data)

    def _validate_inputs(self, input_trace: Trace):
        """
        Validate the input trace and configuration.

        :param input_trace: The input trace to map
        :raises MapperException: If validation fails
        """
        if not all([self.input_format, self.output_format, self.mapping_to_apply]):
            self.logger.error("Incomplete mapping informations", self.log_context)
            raise MapperException(
                "Input format, output format, and mapping configuration must be specified"
            )

        # Check if input_trace match input_format (model validation)
        try:
            self.input_format.value(**input_trace.data)
        except ValidationError as e:
            self.logger.exception("Input format validation failed", e, self.log_context)
            raise InputTraceToModelException("Input format validation failed") from e
        except TypeError as e:
            self.logger.exception(
                "Invalid data type in input trace", e, self.log_context
            )
            raise InputTraceToModelException("Invalid data type in input trace") from e
        except Exception as e:
            self.logger.exception(
                "Input trace does not match the specified input format",
                e,
                self.log_context,
            )
            raise InputTraceToModelException(
                "Input trace does not match the specified input format"
            ) from e
        self.logger.debug("Input trace is valid against his format", self.log_context)

    def _apply_mapping(self, input_data: JsonType) -> JsonType:
        """
        Apply the mapping to the input trace.

        :param input_data: The prepared input data
        :return: The mapped output trace
        """
        # We start from the input trace if the formats are the same
        if self.input_format == self.output_format:
            output_trace = input_data
        else:
            output_trace = {}

        for mapping in self.mapping_to_apply.mappings:
            input_values = []
            for input_field in mapping.input_fields:
                value = get_value_from_flat_key(input_data, input_field)
                input_values.append(value)
            output_trace = self._build_trace_with_output(
                output_content=mapping.output_fields,
                output_trace=output_trace,
                overwrite=True,
                arguments=input_values,
            )
        return output_trace

    def _post_process(self, mapped_data: JsonType) -> JsonType:
        """
        Apply post-processing to the mapped data.

        :param mapped_data: The mapped data to post-process
        :return: The post-processed data
        """
        output_trace = remove_empty_elements(dictionary=mapped_data)
        output_trace = self._apply_default_values(output_trace=output_trace)
        return output_trace

    def _apply_default_values(self, output_trace: JsonType) -> JsonType:
        """
        Apply default values to the output trace.

        :param output_trace: The output trace to apply default values to
        :return: The output trace with default values applied
        """
        self.logger.debug("Apply mapping default values", self.log_context)
        for default_value in self.mapping_to_apply.default_values:
            output_trace = self._build_trace_with_output(
                output_content=default_value, output_trace=output_trace, overwrite=False
            )
        return output_trace

    def _create_output_trace(self, output_data: JsonType) -> Trace:
        """
        Create the final output trace.

        :param output_data: The output data to create the trace from
        :return: The final output trace
        :raises MapperException: If the output trace does not match the specified output format
        """
        self.logger.debug("Create output trace", self.log_context)
        try:
            self.output_format.value(**output_data)
        except ValidationError as e:
            self.logger.exception(
                "Output format validation failed", e, self.log_context
            )
            raise OutputTraceToModelException("Output format validation failed") from e
        except TypeError as e:
            self.logger.exception(
                "Invalid data type in output trace", e, self.log_context
            )
            raise OutputTraceToModelException(
                "Invalid data type in output trace"
            ) from e
        except Exception as e:
            self.logger.exception(
                "Output trace does not match the specified output format",
                e,
                self.log_context,
            )
            raise OutputTraceToModelException(
                "Output trace does not match the specified output format"
            ) from e

        self.logger.info("Mapping done", self.log_context)
        return Trace(
            data=output_data,
            format=CustomTraceFormatStrEnum(self.output_format.name),
            profile=self.profile,
        )

    def _build_trace_with_output(
        self,
        output_content: OutputMappingModel,
        output_trace: dict[str, Any],
        overwrite: bool,
        arguments: list[Any] = None,
    ) -> dict[str, Any]:
        """
        Build the output trace based on the output content.

        :param output_content: The output mapping model
        :param output_trace: The current output trace
        :param overwrite: Whether to overwrite existing values
        :param arguments: Input arguments
        :return: The updated output trace
        """
        if not arguments:
            arguments = []
        outputs = self._handle_output(output_model=output_content, arguments=arguments)
        for output in outputs:
            if output.output_field:
                output_trace = set_value_from_flat_key(
                    dict_list_element=output_trace,
                    flat_key=output.output_field,
                    value=output.value,
                    overwrite=overwrite,
                )
        return output_trace

    def _handle_output(
        self, output_model: OutputMappingModel, arguments: list[Any]
    ) -> list[FinalMappingModel]:
        """
        Handle the output based on the OutputMappingModel.

        :param output_model: The output mapping model
        :param arguments: Input arguments
        :return: List of FinalMappingModel instances
        """
        if output_model.profile:
            self.log_context = {**self.log_context, "profile": self.profile}
            if self.profile is not None:
                self.logger.warning("A profile already exists", self.log_context)
            self.profile = output_model.profile
            self.logger.info("Profile found", self.log_context)

        if output_model.switch:
            return self._apply_switch_transformation(
                switch_value=output_model.switch, arguments=arguments
            )

        if output_model.multiple:
            results = []
            for sub_output in output_model.multiple:
                sub_results = self._handle_output(
                    output_model=sub_output, arguments=arguments
                )
                results.extend(sub_results)
            return results

        if output_model.value:
            value = output_model.value
        elif output_model.custom:
            value = self._apply_custom_transformation(
                custom_input=output_model.custom, arguments=arguments
            )
        else:
            value = arguments[0] if arguments else None

        return [FinalMappingModel(output_field=output_model.output_field, value=value)]

    def _apply_custom_transformation(
        self, custom_input: list[str], arguments: list[Any]
    ) -> Any:
        """
        Apply a series of custom transformations to the input arguments.

        :param custom_input: List of custom transformation strings
        :param arguments: Input arguments for the transformations
        :return: The result of applying all transformations
        :raises MapperException: If there's an error in the custom transformation
        """
        for custom_code in custom_input:
            try:
                transformation = self._eval(expr=custom_code)
                arguments = (
                    transformation(*arguments)
                    if callable(transformation)
                    else transformation
                )
            except Exception as e:
                self.logger.exception(
                    "Error in custom transformation", e, self.log_context
                )
                raise CodeEvaluationException("Error in custom transformation") from e
        return arguments

    @staticmethod
    def _eval(expr: str) -> Callable | Any:
        """
        Evaluate a Python expression.

        TODO : This method should be replaced with a more secure alternative in a production environment.

        :param expr: The expression to evaluate
        :return: The evaluated expression
        """

        return eval(expr)

    def _apply_switch_transformation(
        self,
        switch_value: list[ConditionOutputMappingModel],
        arguments: list[Any] | None = None,
    ) -> list[FinalMappingModel]:
        """
        Apply a switch transformation based on conditions.

        :param switch_value: List of condition-based output mappings
        :param arguments: Input arguments for the conditions
        :return: List of FinalMappingModel instances
        """
        if not arguments:
            arguments = []
        list_response = []

        for condition in switch_value:
            if str(condition.condition).lower().strip() == DEFAULT_CONDITION:
                list_response.extend(
                    self._handle_output(output_model=condition, arguments=arguments)
                )
                return list_response

            try:
                lambda_condition = self._eval(condition.condition)
                if callable(lambda_condition) and lambda_condition(*arguments):
                    list_response.extend(
                        self._handle_output(output_model=condition, arguments=arguments)
                    )
                    return list_response
            except TypeError as e:
                self.logger.exception(
                    "Error in lambda condition",
                    e,
                    {**self.log_context, "condition": condition.condition},
                )
                raise CodeEvaluationException("Error in lambda condition") from e

        list_response.append(FinalMappingModel(output_field=None, value=None))
        return list_response
