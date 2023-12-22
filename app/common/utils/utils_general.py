from typing import Any


def is_empty(x: Any) -> bool:
    """Check a element is empty

    Args:
        x (_type_): element to check

    Returns:
        bool: Element is empty (True) or not (False)
    """
    value = (
        x is None
        or x == ""
        or x == {}
        or x == []
        or str(x).casefold() == "nan".casefold()
        or str(x).casefold() == "none".casefold()
        or str(x).casefold() == "nat".casefold()
        or str(x).casefold() == "null".casefold()
    )
    return value


def replace_empty(value: Any, replace_value: Any = "") -> Any:
    """Replace a value if it's empty

    Args:
        value (Any): Any value
        replace_value (Any, optional): Value to replace with. Defaults to "".

    Returns:
        Any: Either the same value or the replacement value if it's empty
    """
    return replace_value if is_empty(value) else value
