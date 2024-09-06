import pytest
from utils.utils_general import is_empty


@pytest.mark.parametrize(
    "args, expected",
    [
        (None, True),
        ("", True),
        ([], True),
        ({}, True),
        (0, False),
        ("None", True),
        ([None], False),
        ({None}, False),
        (print, False),
        ("Nat", True),
        ("none", True),
        ("null", True),
        ("NaN", True),
        ("This is empty", False),
    ],
)
def test_is_empty(args, expected):
    assert is_empty(args) == expected
