from app.api.schemas import CustomConfigModel
from app.infrastructure.logging.contract import LoggerContract

from .contracts.parser import Parser
from .csv.parser import CSVParser
from .exceptions import ParserFactoryError

MIME_TO_PARSER: dict[str, type[Parser]] = {
    "text/csv": CSVParser,
}


class ParserFactory:
    """
    A factory class for creating parser instances based on MIME types.
    """

    @staticmethod
    def register_parser(mime_type: str, parser_class: type[Parser]):
        """
        Register a new parser class for a specific MIME type.

        :param mime_type: The MIME type to associate with the parser
        :param parser_class: The parser class to register
        """
        MIME_TO_PARSER[mime_type] = parser_class

    @staticmethod
    def get_parser(
        mime_type: str,
        logger: LoggerContract,
        parsing_config: CustomConfigModel | None = None,
    ) -> Parser:
        """
        Get a parser instance for the specified MIME type.

        :param mime_type: The MIME type of the content to parse
        :param logger: LoggerContract implementation for logging
        :param parsing_config: Configuration for the parser
        :return: An instance of the appropriate parser
        :raises ParserFactoryError: If no parser is registered for the given MIME type
        """
        parser_class = MIME_TO_PARSER.get(mime_type)
        if parser_class:
            logger.info("Parser found", {"mime_type": mime_type})
            return parser_class(logger=logger, parsing_config=parsing_config)

        logger.error("Parser not found", {"mime_type": mime_type})
        raise ParserFactoryError(f"Unsupported MIME type: {mime_type}")
