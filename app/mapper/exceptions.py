class MapperError(Exception):
    """Base class for mapper exceptions."""


class MappingConfigToModelError(MapperError):
    """Exception when a mapping config to the Pydantic model fails."""


class CodeEvaluationError(MapperError):
    """Exception when a Python code in Mapping config fails."""
