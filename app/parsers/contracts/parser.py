from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import BinaryIO

from app.api.schemas import CustomConfigModel
from app.common.models.trace import Trace
from app.infrastructure.logging.contract import LoggerContract


class Parser(ABC):
    """
    Abstract base class for all parsers.
    """

    def __init__(
        self, logger: LoggerContract, parsing_config: CustomConfigModel | None = None,
    ):
        """
        Initialize the parser with optional configuration.

        :param logger: LoggerContract implementation for logging
        :param parsing_config: Configuration for the parser
        """

        self.logger = logger
        self.parsing_config = parsing_config or CustomConfigModel()

    @abstractmethod
    def parse(self, file: BinaryIO) -> Iterator[Trace]:
        """
        Parse the given file and yield parsed data.

        :param file: The file-like object to parse
        :yield: Parsed data from the file
        :raises NotImplementedError: If the method is not implemented by subclasses
        """
        raise NotImplementedError
