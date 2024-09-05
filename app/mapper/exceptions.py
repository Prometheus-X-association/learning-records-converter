class MapperException(Exception):
    """Base class for mapper exceptions."""


class MappingConfigToModelException(MapperException):
    """Exception when a mapping config to the Pydantic model fails."""


class InputTraceToModelException(MapperException):
    """Exception when an input trace to his Pydantic model fails."""


class OutputTraceToModelException(MapperException):
    """Exception when the output trace to his Pydantic model fails."""


class CodeEvaluationException(MapperException):
    """Exception when a Python code in Mapping config fails."""
