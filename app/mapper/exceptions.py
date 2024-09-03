class MapperException(Exception):
    """Base class for mapper exceptions."""

    pass


class MappingConfigToModelException(MapperException):
    """Exception when a mapping config to a Pydantic model fails."""

    pass
