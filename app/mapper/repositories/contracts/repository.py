from abc import ABC, abstractmethod
from typing import BinaryIO

from extensions.enums import CustomTraceFormatStrEnum

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
        raise NotImplementedError
