from collections.abc import Callable
from enum import Enum
from typing import Any


class CaseInsensitiveStrEnum(Enum):
    """Case-insensitive when looking for value in enum"""

    # Case-insensitive
    @classmethod
    def _missing_(cls, value) -> "CaseInsensitiveStrEnum | None":
        for member in cls:
            if member.value.lower().strip() == str(value).lower().strip():
                return member
        return None


def extend_enum(*args, enum_class: type[Enum] = Enum) -> Callable[[type[Enum]], Any]:
    """Python does not allow Enum to inherit other Enum.
    This decorator "adds" the list of inherited enums into the decorated enum.

    Args:
        args (List[Enum]): Enums to inherit
        enum_class (type[Enum]): Type of Enum to create
    """

    def wrapper(added_enum):
        joined = {}
        for inherited_enum in args:
            for item in inherited_enum:
                joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return enum_class(added_enum.__name__, joined)

    return wrapper


def str_enum(*args, enum_class: type[Enum] = Enum) -> Callable[[type[Enum]], Any]:
    """Transform an Enum into a StrEnum
    This decorator transforms the list of enums to get all ENUM_KEY = 'enum_key' in one StrEnum.

    Args:
        args (List[Enum]): Enums to inherit
        enum_class (type[Enum]): Type of Enum to create
    """

    def wrapper(added_enum):
        joined = {}
        for inherited_enum in args:
            for item in inherited_enum:
                joined[item.name] = item.name.lower()
        for item in added_enum:
            joined[item.name] = item.name.lower()
        return enum_class(added_enum.__name__, joined)

    return wrapper
