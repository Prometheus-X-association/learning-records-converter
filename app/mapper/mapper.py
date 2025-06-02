from typing import BinaryIO

from app.common.extensions.enums import CustomTraceFormatStrEnum
from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract

from .available_functions.mapping_runnable_functions import get_available_functions
from .evaluator.contract import ExpressionEvaluatorContract
from .exceptions import MapperError
from .mapping_engine import MappingEngine
from .repositories.contracts.repository import MappingRepository


class Mapper:
    """Class responsible for orchestrating the mapping process.

    This class uses a MappingRepository to load schemas and a MappingEngine to perform the actual conversion.
    """

    def __init__(
        self,
        repository: MappingRepository,
        expression_evaluator: ExpressionEvaluatorContract,
        logger: LoggerContract,
    ) -> None:
        """Initialize the Mapper with a MappingRepository.

        :param repository: The repository to use for loading mapping schemas
        :param expression_evaluator: ExpressionEvaluatorContract implementation for Python expressions evaluation
        :param logger: LoggerContract implementation for logging
        """
        self.repository = repository
        self.logger = logger
        self.schema = None

        self.expression_evaluator = expression_evaluator
        available_functions = get_available_functions()
        self.expression_evaluator.register_functions(available_functions)
        self.logger.debug(
            "Registering functions for evaluator",
            {"functions": list(available_functions.keys())},
        )

    def load_schema_by_file(self, file: BinaryIO) -> None:
        """Load a mapping schema from a file.

        :param file: A file-like object containing the mapping schema
        """
        self.schema = self.repository.load_schema_by_file(mapping_file=file)

    def load_schema_by_formats(
        self,
        input_format: CustomTraceFormatStrEnum,
        output_format: CustomTraceFormatStrEnum,
    ) -> None:
        """Load a mapping schema based on input and output formats.

        :param input_format: The format of the input trace
        :param output_format: The desired output format
        """
        self.schema = self.repository.load_schema_by_formats(
            input_format=input_format,
            output_format=output_format,
        )

    def convert(
        self,
        input_trace: Trace,
        output_format: CustomTraceFormatStrEnum,
    ) -> Trace:
        """Convert an input trace to the specified output format.

        :param input_trace: The input trace to be converted
        :param output_format: The desired output format
        :return: The converted trace
        """
        if not self.schema:
            raise MapperError("Mapping schema not loaded")

        engine = MappingEngine(
            logger=self.logger,
            evaluator=self.expression_evaluator,
        )
        return engine.run(
            input_trace=input_trace,
            mapping_to_apply=self.schema,
            output_format=output_format,
        )
