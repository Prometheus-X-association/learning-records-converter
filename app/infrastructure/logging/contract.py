from abc import ABC, abstractmethod
from typing import Any


class LoggerContract(ABC):
    """
    Abstract base class for logger implementations at various severity levels,
    with optional context information.
    """

    @abstractmethod
    def debug(self, message: str, context: dict[str, Any] | None = None) -> None:
        """
        Log a debug message.

        :param message: The message to log
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str, context: dict[str, Any] | None = None) -> None:
        """
        Log an info message.

        :param message: The message to log
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str, context: dict[str, Any] | None = None) -> None:
        """
        Log a warning message.

        :param message: The message to log
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str, context: dict[str, Any] | None = None) -> None:
        """
        Log an error message.

        :param message: The message to log
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError

    @abstractmethod
    def critical(self, message: str, context: dict[str, Any] | None = None) -> None:
        """
        Log a critical message.

        :param message: The message to log
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError

    @abstractmethod
    def exception(
        self,
        message: str,
        exc: Exception,
        context: dict[str, Any] | None = None,
    ) -> None:
        """
        Log an exception.

        :param message: A descriptive message about the exception
        :param exc: The exception object
        :param context: Additional contextual information to include with the log.
        """
        raise NotImplementedError
