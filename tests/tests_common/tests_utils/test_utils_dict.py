import pytest
from utils.utils_dict import (
    get_nested_from_flat,
    get_value_from_flat_key,
    remove_empty_elements,
    set_value_from_flat_key,
)


##################################################
#           set_value_from_flat_key
##################################################
@pytest.mark.parametrize(
    "args, expected",
    [
        (
            {
                "json_lo": {"age": {"min": 3, "max": 30}},
                "flat_key": "age",
                "value": {"min": 15, "max": 150},
                "overwrite": True,
            },
            {"age": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"age": {"min": 3, "max": 30}},
                "flat_key": "age",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"age": {"min": 3, "max": 30}},
        ),
        (
            {
                "json_lo": {"number": 45},
                "flat_key": "number.age",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"number": 45},
        ),
        (
            {
                "json_lo": {},
                "flat_key": "age",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"age": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"age": None},
                "flat_key": "age",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"age": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"test": "oui"},
                "flat_key": "inokufu.3.age",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "oui", "inokufu": [None, None, None, {"age": {"min": 15, "max": 150}}]},
        ),
        (
            {
                "json_lo": {"test": "non"},
                "flat_key": "inokufu.7",
                "value": {"min": 15, "max": 150},
                "overwrite": True,
            },
            {
                "test": "non",
                "inokufu": [None, None, None, None, None, None, None, {"min": 15, "max": 150}],
            },
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": [13]},
                "flat_key": "inokufu.4",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [13, None, None, None, {"min": 15, "max": 150}]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": [13]},
                "flat_key": "inokufu.0",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [13]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": [13]},
                "flat_key": "inokufu.1",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [13, {"min": 15, "max": 150}]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": ""},
                "flat_key": "inokufu",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": ""},
                "flat_key": "inokufu.0",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [{"min": 15, "max": 150}]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": None},
                "flat_key": "inokufu.0",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [{"min": 15, "max": 150}]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": {}},
                "flat_key": "inokufu.0",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": [{"min": 15, "max": 150}]},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": {}},
                "flat_key": "inokufu",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": None},
                "flat_key": "inokufu",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": {"min": 15, "max": 150}},
        ),
        (
            {
                "json_lo": {"test": "non", "inokufu": []},
                "flat_key": "inokufu",
                "value": {"min": 15, "max": 150},
                "overwrite": False,
            },
            {"test": "non", "inokufu": {"min": 15, "max": 150}},
        ),
    ],
)
def test_set_value_from_flat_key(args, expected):
    assert (
        set_value_from_flat_key(
            args["json_lo"], args["flat_key"], args["value"], args["overwrite"]
        )
        == expected
    )


##################################################
#           get_value_from_flat_key
##################################################
@pytest.mark.parametrize(
    "args, expected",
    [
        (
            {
                "json_lo": {"age": {"min": 3, "max": 30}},
                "flat_key": "age",
            },
            {"min": 3, "max": 30},
        ),
        (
            {
                "json_lo": {"age": {"min": 3, "max": 30}},
                "flat_key": "",
            },
            None,
        ),
        (
            {
                "json_lo": {"age": {"min": ["one", "two", "three"], "max": 30}},
                "flat_key": "age.min.1",
            },
            "two",
        ),
        (
            {
                "json_lo": {"age": {"min": 3, "max": 30}},
                "flat_key": "age.mean",
            },
            None,
        ),
        (
            {
                "json_lo": {"age": {"min": {}, "max": 30}},
                "flat_key": "age.min",
            },
            {},
        ),
        (
            {
                "json_lo": {"age": {"min": ["one", "two", "three"], "max": 30}},
                "flat_key": "age.min.4",
            },
            None,
        ),
        (
            {
                "json_lo": {"age": {"min": [], "max": 30}},
                "flat_key": "age.min.one.next.key",
                "default_value": "DEFAULT_VALUE",
            },
            "DEFAULT_VALUE",
        ),
        (
            {
                "json_lo": {
                    "age": {"min": [{"one": "two"}, {"three": "four"}, {"five": "six"}], "max": 30}
                },
                "flat_key": "age.min.2.five",
            },
            "six",
        ),
    ],
)
def test_get_value_from_flat_key(args, expected):
    params = {
        "dict_element": args["json_lo"],
        "flat_key": args["flat_key"],
    }
    if "default_value" in args:
        params["default_value"] = args.get("default_value")
    if "return_copy" in args:
        params["return_copy"] = args.get("return_copy")
    assert get_value_from_flat_key(**params) == expected


# TODO:
"""
get_nested_from_flat
remove_empty_elements,
get_nested_from_flat,
"""
