import pytest
from utils.utils_dict import (
    drop_duplicates_in_list_on_field,
    get_flat_from_nested,
    get_nested_from_flat,
    get_value_from_first_key_available,
    get_value_from_flat_key,
    is_flat_key_in_dict,
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


##################################################
#           get_value_from_first_key_available
##################################################
@pytest.mark.parametrize(
    "args, expected",
    [
        (
            {
                "json_element": {"codepostal": {"code": "90", "base": "Nom", "test": "oui"}},
                "base_field": "codepostal",
                "keys_tuple": ("code", "base"),
            },
            ("90", "codepostal.code"),
        ),
        (
            {
                "json_element": {"codepostal": {"code": "", "base": "Nom", "test": "oui"}},
                "base_field": "codepostal",
                "keys_tuple": ("code", "base"),
            },
            ("Nom", "codepostal.base"),
        ),
        (
            {
                "json_element": {"codepostal": {"code": "90", "base": "Nom", "test": "oui"}},
                "base_field": "codepostal",
                "keys_tuple": ("non", "autre", "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": {},
                "base_field": "codepostal",
                "keys_tuple": ("non", "autre", "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": None,
                "base_field": "codepostal",
                "keys_tuple": ("non", "autre", "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": {"codepostal": {"code": "90", "base": "Nom", "test": "oui"}},
                "base_field": "department",
                "keys_tuple": ("non", "autre", "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": "",
                "keys_tuple": ("autre", "non", "inokufu"),
            },
            ("test externe", "non"),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": None,
                "keys_tuple": ("autre", "non", "inokufu"),
            },
            ("test externe", "non"),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": None,
                "keys_tuple": ["autre", None, "inokufu"],
            },
            ("", ""),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": None,
                "keys_tuple": ["autre", "non", "inokufu"],
            },
            ("test externe", "non"),
        ),
        (
            {
                "json_element": ["inofuku", "codepostal"],
                "base_field": None,
                "keys_tuple": ("autre", "non", "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": "codepostal",
                "keys_tuple": ("autre", ["non"], "inokufu"),
            },
            ("", ""),
        ),
        (
            {
                "json_element": {
                    "codepostal": {"code": "90", "base": "Nom", "test": "oui"},
                    "non": "test externe",
                },
                "base_field": "codepostal",
                "keys_tuple": ("autre", ["non"], 8.9, {"test2": "dico"}, ("tuple", "secondaire")),
            },
            ("", ""),
        ),
    ],
)
def test_get_value_from_first_key_available(args, expected):
    assert (
        get_value_from_first_key_available(
            args["json_element"], args["base_field"], args["keys_tuple"]
        )
        == expected
    )


# TODO:
"""
get_flat_from_nested,
remove_empty_elements,
get_nested_from_flat,
drop_duplicates_in_list_on_field,
is_flat_key_in_dict,
"""
