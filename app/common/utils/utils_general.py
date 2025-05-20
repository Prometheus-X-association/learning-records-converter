from typing import Any

EMPTY_STRINGS = {"nan", "none", "nat", "null", ""}


def is_empty(x: Any) -> bool:
    """Check if an element is empty.

    Args:
        x (_type_): element to check

    Returns:
        bool: Element is empty (True) or not (False)

    """
    if x is None:
        return True
    if isinstance(x, str | list | dict | set | tuple):
        return len(x) == 0
    return str(x).lower() in EMPTY_STRINGS


def replace_empty(value: Any, replace_value: Any = "") -> Any:
    """Replace a value if it's empty.

    Args:
        value (Any): Any value
        replace_value (Any, optional): Value to replace with. Defaults to "".

    Returns:
        Any: Either the same value or the replacement value if it's empty

    """
    return replace_value if is_empty(value) else value
