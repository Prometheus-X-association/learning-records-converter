class ProfilerException(Exception):
    """Base class for profiler exceptions."""
    pass


class ProfileNotFoundException(ProfilerException):
    """Exception when a profile is not found."""
    pass


class TemplateNotFoundException(ProfilerException):
    """Exception when a template is not found."""
    pass


class InvalidJsonException(ProfilerException):
    """Exception when a JSON profile is invalid."""
    pass


class ProfileValidationError(ProfilerException):
    """Exception when a profile is not validated by Pydantic."""
    pass
