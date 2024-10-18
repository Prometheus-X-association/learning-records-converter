from abc import ABC, abstractmethod
from typing import BinaryIO

from extensions.enums import CustomTraceFormatStrEnum
from pydantic import ValidationError

from app.mapper.exceptions import MappingConfigToModelError
from app.mapper.models.mapping_schema import MappingSchema


class MappingRepository(ABC):
    """
    Abstract base class for mapping repositories.

    This class defines the interface for loading and checking the existence of mapping schemas.
    """

    @abstractmethod
    def load_schema_by_formats(
        self,
        input_format: CustomTraceFormatStrEnum,
        output_format: CustomTraceFormatStrEnum,
    ) -> MappingSchema:
        """
        Load a mapping schema for the given input and output formats.

        :param input_format: The format of the input trace
        :param output_format: The desired output format
        :return: The loaded mapping schema
        """
        raise NotImplementedError

    @abstractmethod
    def load_schema_by_file(self, mapping_file: BinaryIO) -> MappingSchema:
        """
        Load a mapping schema from a file.

        :param mapping_file: A file-like object containing the mapping schema
        :return: The parsed mapping schema
        """
        raise NotImplementedError

    @staticmethod
    def get_mapping_model(config: dict) -> MappingSchema:
        """
        Load and validate a configuration dict into a MappingSchema.

        :param config: The mapping configuration dictionary
        :return: A validated MappingSchema instance
        :raises MappingConfigToModelError: If the configuration is invalid
        """
        try:
            return MappingSchema(**config)
        except ValidationError as e:
            raise MappingConfigToModelError("Mapping validation failed") from e
        except (TypeError, ValueError, KeyError) as e:
            raise MappingConfigToModelError("Invalid data type in mapping") from e
