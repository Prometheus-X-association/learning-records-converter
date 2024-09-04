from abc import ABC, abstractmethod

from app.common.enums import CustomTraceFormatStrEnum
from app.mapper.mapping_schema import MappingSchema


class MappingRepository(ABC):
    """
    Abstract base class for mapping repositories.

    This class defines the interface for loading and checking the existence of mapping schemas.
    """

    @abstractmethod
    def load_schema(
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

        ...
