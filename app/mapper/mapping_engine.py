from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from extensions.enums import CustomTraceFormatStrEnum
from utils.utils_dict import (
    get_value_from_flat_key,
    remove_empty_elements,
    set_value_from_flat_key,
)

from app.common.common_types import JsonType
from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract

from .evaluator.contract import ExpressionEvaluatorContract
from .models.mapping_models import FinalMappingModel
from .models.mapping_schema import (
    ConditionOutputMappingModel,
    MappingSchema,
    OutputMappingModel,
)

DEFAULT_CONDITION = "default"


class MappingEngine:
    """Handles mapping from an input format to an output format using a config model."""

    def __init__(
        self,
        evaluator: ExpressionEvaluatorContract,
        logger: LoggerContract,
    ) -> None:
        """
        Initialize the MappingEngine.

        :param evaluator: ExpressionEvaluatorContract implementation for Python expressions evaluation
        :param logger: LoggerContract implementation for logging
        """
        self.evaluator = evaluator
        self.logger = logger
        self.log_context: dict[str, str] = {}
        self.profile: str | None = None

    def run(
        self,
        input_trace: Trace,
        mapping_to_apply: MappingSchema,
        output_format: CustomTraceFormatStrEnum,
    ) -> Trace:
        """
        Main function : run the mapping process on the input trace.

        :param input_trace: The input trace to map
        :param mapping_to_apply: The mapping configuration to apply
        :param output_format: The desired output format
        :return: The mapped output trace
        """
        self.log_context = {
            "input_format": input_trace.format.name,
            "output_format": output_format.name,
        }

        mapped_data = self._apply_mapping(
            input_trace=input_trace,
            mapping_schema=mapping_to_apply,
            output_format=output_format,
        )
        output_data = self._post_process(
            mapped_data=mapped_data,
            mapping_schema=mapping_to_apply,
        )
        output_trace = self._create_output_trace(
            output_data=output_data,
            output_format=output_format,
        )

        self.logger.info("Mapping done", self.log_context)

        return output_trace

    def _apply_mapping(
        self,
        input_trace: Trace,
        mapping_schema: MappingSchema,
        output_format: CustomTraceFormatStrEnum,
    ) -> JsonType:
        """
        Apply the mapping to the input trace.

        :param input_trace: The prepared input trace
        :param mapping_schema: The mapping schema to apply
        :param output_format: The desired output format
        :return: The mapped output trace
        """
        input_data = input_trace.data

        # We start from the input trace if the formats are the same
        output_data = input_data if input_trace.format == output_format else {}

        for mapping in mapping_schema.mappings:
            input_values = []
            for input_field in mapping.input_fields:
                value = get_value_from_flat_key(input_data, input_field)
                input_values.append(value)
            output_data = self._build_trace_with_output(
                output_content=mapping.output_fields,
                output_data=output_data,
                overwrite=True,
                arguments=input_values,
            )
        return output_data

    def _post_process(
        self,
        mapped_data: JsonType,
        mapping_schema: MappingSchema,
    ) -> JsonType:
        """
        Apply post-processing to the mapped data.

        :param mapped_data: The mapped data to post-process
        :param mapping_schema: The mapping schema to apply
        :return: The post-processed data
        """
        output_data = remove_empty_elements(dictionary=mapped_data)
        return self._apply_default_values(
            output_data=output_data,
            mapping_schema=mapping_schema,
        )

    def _apply_default_values(
        self,
        output_data: JsonType,
        mapping_schema: MappingSchema,
    ) -> JsonType:
        """
        Apply default values to the output data.

        :param output_data: The output trace to apply default values to
        :param mapping_schema: The mapping schema to apply
        :return: The output data with default values applied
        """
        self.logger.debug("Apply mapping default values", self.log_context)
        for default_value in mapping_schema.default_values:
            output_data = self._build_trace_with_output(
                output_content=default_value,
                output_data=output_data,
                overwrite=False,
            )
        return output_data

    def _create_output_trace(
        self,
        output_data: JsonType,
        output_format: CustomTraceFormatStrEnum,
    ) -> Trace:
        """
        Create the final output trace.

        :param output_data: The output data to create the trace from
        :param output_format: The desired output format
        :return: The final output trace
        """
        self.logger.debug("Create output trace", self.log_context)

        return Trace(
            data=output_data,
            format=output_format,
            profile=self.profile,
        )

    def _build_trace_with_output(
        self,
        output_content: OutputMappingModel,
        output_data: Mapping[str, Any],
        overwrite: bool,
        arguments: Sequence[Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build the output trace based on the output content.

        :param output_content: The output mapping model
        :param output_data: The current output trace
        :param overwrite: Whether to overwrite existing values
        :param arguments: Input arguments
        :return: The updated output trace
        """
        if not arguments:
            arguments = []
        outputs = self._handle_output(output_model=output_content, arguments=arguments)
        for output in outputs:
            if output.output_field:
                output_data = set_value_from_flat_key(
                    dict_list_element=output_data,
                    flat_key=output.output_field,
                    value=output.value,
                    overwrite=overwrite,
                )
        return output_data

    def _handle_output(
        self,
        output_model: OutputMappingModel,
        arguments: Sequence[Any],
    ) -> list[FinalMappingModel]:
        """
        Handle the output based on the OutputMappingModel.

        :param output_model: The output mapping model
        :param arguments: Input arguments
        :return: List of FinalMappingModel instances
        """
        if output_model.profile:
            self.log_context = {**self.log_context, "profile": output_model.profile}
            if self.profile is not None:
                self.logger.warning("A profile already exists", self.log_context)
            self.profile = output_model.profile
            self.logger.info("Profile found", self.log_context)

        if output_model.switch:
            return self._apply_switch_transformation(
                switch_value=output_model.switch,
                arguments=arguments,
            )

        if output_model.multiple:
            results = []
            for sub_output in output_model.multiple:
                sub_results = self._handle_output(
                    output_model=sub_output,
                    arguments=arguments,
                )
                results.extend(sub_results)
            return results

        if output_model.value:
            value = output_model.value
        elif output_model.custom:
            value = self._apply_custom_transformation(
                custom_input=output_model.custom,
                arguments=arguments,
            )
        else:
            value = arguments[0] if arguments else None

        return [FinalMappingModel(output_field=output_model.output_field, value=value)]

    def _apply_custom_transformation(
        self,
        custom_input: Iterable[str],
        arguments: Sequence[Any],
    ) -> Any:
        """
        Apply a series of custom transformations to the input arguments.

        :param custom_input: Iterable of custom transformation strings
        :param arguments: Input arguments for the transformations
        :return: The result of applying all transformations
        :raises CodeEvaluationError: If there's an error in the custom transformation
        """
        result = arguments
        for custom_code in custom_input:
            if custom_code.startswith("lambda"):
                # Use the evaluator for lambda expressions
                result = self.evaluator.eval_lambda(custom_code, *result)
            else:
                # Use the evaluator for regular expressions
                result = self.evaluator.eval_expression(expression=custom_code)
        return result

    def _apply_switch_transformation(
        self,
        switch_value: Iterable[ConditionOutputMappingModel],
        arguments: Sequence[Any] | None = None,
    ) -> list[FinalMappingModel]:
        """
        Apply a switch transformation based on conditions.

        :param switch_value: Iterable of condition-based output mappings
        :param arguments: Input arguments for the conditions
        :return: List of FinalMappingModel instances
        :raises CodeEvaluationError: If there's an error in the lambda condition
        """
        if not arguments:
            arguments = []
        list_response = []

        for condition in switch_value:
            if str(condition.condition).lower().strip() == DEFAULT_CONDITION:
                list_response.extend(
                    self._handle_output(output_model=condition, arguments=arguments),
                )
                return list_response

            condition_result = self.evaluator.eval_lambda(
                condition.condition,
                *arguments,
            )
            if condition_result:
                list_response.extend(
                    self._handle_output(output_model=condition, arguments=arguments),
                )
                return list_response

        list_response.append(FinalMappingModel(output_field=None, value=None))
        return list_response
