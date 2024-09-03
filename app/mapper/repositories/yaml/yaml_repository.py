from pathlib import Path

from pydantic import ValidationError
from trace_formats.enums import TraceFormatEnum
from utils.utils_dict import convert_yaml_file_to_json

from app.common.enums import (CustomTraceFormatModelEnum,
                              CustomTraceFormatOutputMappingEnum,
                              CustomTraceFormatStrEnum)
from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract
from app.mapper.exceptions import MappingConfigToModelException
from app.mapper.repositories.contracts.repository import MappingRepository
from app.xapi_converter.transformer.mapping_input import MappingInput

from .mapping_config import CompleteConfigModel


class YamlMappingRepository(MappingRepository):
    """
    A concrete implementation of MappingRepository that uses YAML configuration files for mapping.

    This class handles the conversion of traces based on YAML mapping configurations.

    :param logger: An instance of LoggerContract for logging
    """

    def __init__(self, logger: LoggerContract):
        self.logger = logger

    def convert(
        self, input_trace: Trace, output_format: CustomTraceFormatStrEnum
    ) -> Trace:
        """
        Convert an input trace to the specified output format using YAML mapping configurations.

        :param input_trace: The input trace to be converted
        :param output_format: The desired output format for the trace
        :return: The converted trace
        :raises ValueError: If the mapping configuration is not found
        """

        log_context = {
            "input_format": input_trace.format,
            "output_format": output_format,
        }

        mapping_path = self._get_mapping_by_input_and_output_format(
            input_format=input_trace.format, output_format=output_format
        )
        mapping_config = self._get_config_model_from_yaml_file(file_path=mapping_path)

        self.logger.debug("Mapping start", log_context)
        mapping = MappingInput(
            input_format=CustomTraceFormatModelEnum[input_trace.format.name],
            mapping_to_apply=mapping_config,
            output_format=CustomTraceFormatModelEnum[output_format.name],
        )
        output_trace = mapping.run(input_trace=input_trace)
        self.logger.info("Mapping done", log_context)

        return output_trace

    def _get_mapping_by_input_and_output_format(
        self,
        input_format: CustomTraceFormatStrEnum,
        output_format: CustomTraceFormatStrEnum,
    ) -> Path:
        """
        Retrieve the correct mapping configuration file path based on input and output formats.

        :param input_format: The format of the input trace
        :param output_format: The desired output format
        :return: The path to the mapping configuration file
        :raises ValueError: If the mapping configuration is not found
        """

        # Get correct mapping enum
        log_context = {
            "output_format": output_format.value,
            "input_format": input_format.value,
        }
        self.logger.debug("Search mapping path", log_context)

        try:
            output_format_mappings = CustomTraceFormatOutputMappingEnum[
                output_format.name
            ].value
        except (ValueError, KeyError) as e:
            self.logger.exception("Mapping not found", e, log_context)
            raise ValueError(f"Output mapping enum to {output_format} not found")

        try:
            mapping_config = output_format_mappings[input_format.name]
        except (ValueError, KeyError) as e:
            self.logger.exception("Mapping config not found", e, log_context)
            raise ValueError(
                f"Mapping from {input_format} to {output_format} not found"
            )

        # Read config file
        if isinstance(mapping_config, TraceFormatEnum):
            mapping_path = mapping_config.value
        else:
            self.logger.error("Mapping model not found", log_context)
            raise ValueError("Could not load mapping config into model")

        log_context.update({"mapping_path": mapping_path})
        self.logger.debug("Mapping path found", log_context)

        return Path(mapping_path)

    def _get_config_model_from_yaml_file(self, file_path: Path) -> CompleteConfigModel:
        """
        Load and validate a YAML configuration file into a CompleteConfigModel.

        :param file_path: The path to the YAML configuration file
        :return: A validated CompleteConfigModel instance
        :raises MappingConfigToModelException: If the configuration file is invalid or cannot be loaded
        """
        json_config = convert_yaml_file_to_json(yaml_path=file_path)
        self.logger.info("Mapping config loaded", {"path": file_path})
        # Load mapping in Model
        try:
            return CompleteConfigModel(**json_config)
        except ValidationError as e:
            self.logger.exception("Mapping validation failed", e)
            raise MappingConfigToModelException(
                f"Mapping validation failed: {e}"
            ) from e
        except TypeError as e:
            self.logger.exception("Invalid data type in mapping", e)
            raise MappingConfigToModelException(
                f"Invalid data type in profile: {e}"
            ) from e
        except Exception as e:
            self.logger.exception("Unexpected error during mapping file validation", e)
            raise MappingConfigToModelException(
                f"Unexpected error during profile validation: {e}"
            ) from e
