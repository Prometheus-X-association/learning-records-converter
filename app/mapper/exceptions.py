class MapperException(Exception):
    """Base class for mapper exceptions."""

    pass


class MappingConfigToModelException(MapperException):
    """Exception when a mapping config to the Pydantic model fails."""

    pass


class InputTraceToModelException(MapperException):
    """Exception when an input trace to his Pydantic model fails."""

    pass


class OutputTraceToModelException(MapperException):
    """Exception when the output trace to his Pydantic model fails."""

    pass


class CodeEvaluationException(MapperException):
    """Exception when a Python code in Mapping config fails."""

    pass
