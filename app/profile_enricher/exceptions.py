class ProfilerException(Exception):
    """Base class for profiler exceptions."""


class ProfileNotFoundException(ProfilerException):
    """Exception when a profile is not found."""


class TemplateNotFoundException(ProfilerException):
    """Exception when a template is not found."""


class InvalidJsonException(ProfilerException):
    """Exception when a JSON profile is invalid."""


class ProfileValidationError(ProfilerException):
    """Exception when a profile is not validated by Pydantic."""


class BasePathException(ProfilerException):
    """Exception for errors related to the base path for profiles."""
