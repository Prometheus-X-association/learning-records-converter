class ProfilerError(Exception):
    """Base class for profiler exceptions."""


class ProfileNotFoundError(ProfilerError):
    """Exception when a profile is not found."""


class TemplateNotFoundError(ProfilerError):
    """Exception when a template is not found."""


class InvalidJsonError(ProfilerError):
    """Exception when a JSON profile is invalid."""


class ProfileValidationError(ProfilerError):
    """Exception when a profile is not validated by Pydantic."""


class BasePathError(ProfilerError):
    """Exception for errors related to the base path for profiles."""
