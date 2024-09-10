import json
import logging
import sys
from typing import Any

from .contract import LoggerContract


class JsonLoggingFormatter(logging.Formatter):
    """
    Custom formatter that outputs log records in a JSON format.

    This formatter includes timestamp, log level, message, and any additional context
    provided in the log record.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record as JSON.

        :param record: The log record to format.
        :return: A JSON string representing the formatted log record.
        """
        log_data = {
            "timestamp": self.formatTime(record=record, datefmt=self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        return json.dumps(obj=log_data, default=str)


class JsonLogger(LoggerContract):
    """
    Concrete implementation of LoggerContract using Python's built-in logging module.

    This implementation formats logs as JSON and supports adding context to log messages.
    """

    def __init__(self, name: str, level: str) -> None:
        """
        Initialize the JsonLogger.

        :param name: The name of the logger, typically __name__ of the calling module.
        :param level: The minimum log level to output
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonLoggingFormatter())
        self._logger.addHandler(handler)

    def _log(
        self, level: int, message: str, context: dict[str, Any] | None = None,
    ) -> None:
        """
        Internal method to handle logging at different levels.

        :param level: The logging level (e.g., logging.INFO, logging.ERROR).
        :param message: The message to log.
        :param context: Additional contextual information to include with the log.
        """
        extra = {"context": context} if context else {}
        self._logger.log(level=level, msg=message, extra=extra)

    def debug(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Inherited from LoggerContract.debug."""
        self._log(level=logging.DEBUG, message=message, context=context)

    def info(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Inherited from LoggerContract.info."""
        self._log(level=logging.INFO, message=message, context=context)

    def warning(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Inherited from LoggerContract.warning."""
        self._log(level=logging.WARNING, message=message, context=context)

    def error(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Inherited from LoggerContract.error."""
        self._log(level=logging.ERROR, message=message, context=context)

    def critical(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Inherited from LoggerContract.critical."""
        self._log(level=logging.CRITICAL, message=message, context=context)

    def exception(
        self, message: str, exc: Exception, context: dict[str, Any] | None = None,
    ) -> None:
        """Inherited from LoggerContract.exception."""
        exc_context = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }
        if context:
            exc_context.update(context)
        self.error(message, exc_context)
