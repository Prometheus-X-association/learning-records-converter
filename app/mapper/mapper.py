from extensions.enums import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum

from app.common.models.trace import Trace

from .mapping_engine import MappingEngine
from .repositories.contracts.repository import MappingRepository


class Mapper:
    """
    Class responsible for orchestrating the mapping process.

    This class uses a MappingRepository to load schemas and a MappingEngine to perform the actual conversion.
    """

    def __init__(self, repository: MappingRepository):
        """
        Initialize the Mapper with a MappingRepository.

        :param repository: The repository to use for loading mapping schemas
        """
        self.repository = repository

    def convert(
        self, input_trace: Trace, output_format: CustomTraceFormatStrEnum
    ) -> Trace:
        """
        Convert an input trace to the specified output format.

        :param input_trace: The input trace to be converted
        :param output_format: The desired output format
        :return: The converted trace
        """
        schema = self.repository.load_schema(
            input_format=input_trace.format, output_format=output_format
        )

        engine = MappingEngine(
            input_format=CustomTraceFormatModelEnum[input_trace.format.name],
            mapping_to_apply=schema,
            output_format=CustomTraceFormatModelEnum[output_format.name],
        )
        converted_trace = engine.run(input_trace=input_trace)
        return converted_trace
