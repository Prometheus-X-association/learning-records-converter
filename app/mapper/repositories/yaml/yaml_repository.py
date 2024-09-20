from pathlib import Path
from typing import BinaryIO

import yaml
from enums import TraceFormatEnum
from extensions.enums import (
    CustomTraceFormatOutputMappingEnum,
    CustomTraceFormatStrEnum,
)
from pydantic import ValidationError
from utils.utils_dict import convert_yaml_file_to_json

from app.infrastructure.logging.contract import LoggerContract
from app.mapper.exceptions import MappingConfigToModelError
from app.mapper.models.mapping_schema import MappingSchema
from app.mapper.repositories.contracts.repository import MappingRepository


class YamlMappingRepository(MappingRepository):
    """
    A concrete implementation of MappingRepository that uses YAML configuration files for mapping.

    This class handles the loading of mapping schemas from YAML files based on input and output formats.
    """

    def __init__(self, logger: LoggerContract) -> None:
        """
        Initialize the YamlMappingRepository.

        :param logger: An instance of LoggerContract for logging
        """
        self.logger = logger

    def load_schema_by_formats(
        self,
        input_format: CustomTraceFormatStrEnum,
        output_format: CustomTraceFormatStrEnum,
    ) -> MappingSchema:
        """
        Load a mapping schema for the given input and output formats from a YAML file.

        :param input_format: The format of the input trace
        :param output_format: The desired output format
        :return: The loaded mapping schema
        :raises ValueError: If the mapping configuration is not found
        :raises MappingConfigToModelException: If the configuration file is invalid or cannot be loaded
        """
        mapping_path = self._get_mapping_by_input_and_output_format(
            input_format=input_format,
            output_format=output_format,
        )

        json_config = convert_yaml_file_to_json(yaml_path=mapping_path)
        self.logger.info("Mapping config loaded", {"path": mapping_path})

        return self._get_config_model(config=json_config)

    def load_schema_by_file(self, mapping_file: BinaryIO) -> MappingSchema:
        contents = mapping_file.read()
        json_config = yaml.safe_load(contents)

        return self._get_config_model(config=json_config)

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
            msg = "Output mapping not found"
            self.logger.exception(msg, e, log_context)
            raise ValueError(msg) from e

        try:
            mapping_config = output_format_mappings[input_format.name]
        except (ValueError, KeyError) as e:
            msg = "Mapping config not found"
            self.logger.exception(msg, e, log_context)
            raise ValueError(msg) from e

        # Read config file
        if isinstance(mapping_config, TraceFormatEnum) or not mapping_config.value:
            mapping_path = mapping_config.value
        else:
            msg = "Mapping model not found"
            self.logger.error(msg, log_context)
            raise ValueError(msg)

        self.logger.debug(
            "Mapping path found",
            {**log_context, "mapping_path": mapping_path},
        )

        return Path(mapping_path)

    def _get_config_model(self, config: dict) -> MappingSchema:
        """
        Load and validate a configuration dict into a MappingSchema.

        :param config: The mapping configuration
        :return: A validated CompleteConfigModel instance
        :raises MappingConfigToModelError: If the configuration file is invalid or cannot be loaded
        """
        # Load mapping in Model
        try:
            return MappingSchema(**config)
        except ValidationError as e:
            msg = "Mapping validation failed"
            self.logger.exception(msg, e)
            raise MappingConfigToModelError(msg) from e
        except TypeError as e:
            msg = "Invalid data type in mapping"
            self.logger.exception(msg, e)
            raise MappingConfigToModelError(msg) from e
        except Exception as e:
            msg = "Unexpected error during mapping file validation"
            self.logger.exception(msg, e)
            raise MappingConfigToModelError(msg) from e
