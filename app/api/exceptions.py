class LRCAPIException(Exception):
    """Base exception for LRC API errors."""

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class InternalServerError(LRCAPIException):
    """Exception raised for internal server errors."""

    def __init__(self, *args: object) -> None:
        super().__init__("Something went wrong, please contact our support.", *args)


class NotFoundElementError(LRCAPIException):
    """Exception raised when a requested element is not found."""

    def __init__(self, element: str, *args: object) -> None:
        super().__init__(f"Element not found: {element}", *args)


class BadRequestError(LRCAPIException):
    """Exception raised for malformed requests."""

    def __init__(self, detail: str, *args: object) -> None:
        super().__init__(f"Bad request: {detail}", *args)


class ForbiddenError(LRCAPIException):
    """Exception raised when access is forbidden."""

    def __init__(self, reason: str = "Access denied", *args: object) -> None:
        super().__init__(f"Forbidden: {reason}", *args)
