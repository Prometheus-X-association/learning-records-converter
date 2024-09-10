import contextlib
import re
from pathlib import Path
from typing import Any, overload

import yaml

from .utils_general import is_empty


@overload
def remove_empty_elements(dictionary: list) -> list: ...


@overload
def remove_empty_elements(dictionary: dict) -> dict: ...


def remove_empty_elements(dictionary: list | dict) -> list | dict:
    """Remove empty fields.

    Args:
        dictionary : dictionary to remove empty fields

    Returns:
        dictionnary with removed fields
    """
    if not isinstance(dictionary, dict | list):
        return dictionary
    if isinstance(dictionary, list):
        return [
            value
            for value in (remove_empty_elements(value) for value in dictionary)
            if not is_empty(value)
        ]
    return {
        key: value
        for key, value in (
            (key, remove_empty_elements(value)) for key, value in dictionary.items()
        )
        if not is_empty(value)
    }


def get_value_from_flat_key(
    dict_element: dict | list,
    flat_key: str,
    default_value=None,
    return_copy=True,
) -> Any:
    """Get value from a dict element by using a flatten key (keys separated with dotes)
    If the value exists (even if it's empty), the method returns the value.
    Else, the 'default_value' is returned.

    TODO :
        - use default_value really when value does not exist

    Args:
        dict_element (dict): Dict to navigate
        flat_key (str): Flatten key (key1.key2)
        default_value (Any): Default value if ever nothing is found. Default value is None
        return_copy (bool): Return a copy if type is dict or list. Default value is True

    Returns:
        Any: Value or None if nothing was found.
    """
    list_key = flat_key.split(".")
    total_list_key_len = len(list_key)
    value = dict_element if not is_empty(dict_element) else {}
    for index, key in enumerate(list_key, start=1):
        if key.isnumeric() and isinstance(value, list):
            try:
                value = value[int(key)]
            except IndexError:
                value = default_value
        elif not key.isnumeric() and isinstance(value, dict):
            value = value.get(key, default_value)
        else:
            value = default_value
        if not value:
            if index < total_list_key_len:
                value = default_value
            break
    if return_copy and isinstance(value, list | dict):
        return value.copy()
    return value


@overload
def set_value_from_flat_key(
    dict_list_element: dict,
    flat_key: str,
    value: Any,
    overwrite: bool = True,
) -> dict: ...


@overload
def set_value_from_flat_key(
    dict_list_element: list,
    flat_key: str,
    value: Any,
    overwrite: bool = True,
) -> list: ...


def set_value_from_flat_key(
    dict_list_element: dict | list,
    flat_key: str,
    value: Any,
    overwrite: bool = True,
) -> dict | list:
    """
    Set recursively a value into a dict element by using a flatten key (keys separated with dotes).
    Integer (numeric) are considered as list indexes.

    TODO :
        New argument : preserve_type? : bool -> set only if type is the same.

    Args:
        dict_list_element (Union[dict, list]): Dict of list to navigate.
        flat_key (str): Flatten key (key1.key2).
        value (Any): Value to set.
        overwrite (bool, optional): If True, overwrite existing value if any.
            Defaults to True.
            If overwrite is False, it will not overwrite any non-empty field.

    Raises:
        ValueError: Raised if error during flat_key splitting.

    Returns:
        Union[dict, list]: The original dict or list, modified if not overwrite.
    """
    list_key = re.split(r"(?<!\\)\.", flat_key)

    # If there is at least one key to navigate
    if not is_empty(flat_key) and len(list_key) > 0:
        first_key = list_key.pop(0)
        first_key = first_key.replace(r"\.", ".")

        # If not overwrite but found element is not list, dict or None, return
        if (
            not overwrite
            and not isinstance(dict_list_element, list | dict)
            and not is_empty(dict_list_element)  # before : None
        ):
            # Return current value
            return dict_list_element

        # Numeric keys (list)
        if first_key.isnumeric():
            index = int(first_key)
            # If not list, create one
            if not isinstance(dict_list_element, list):
                dict_list_element = []
            # If all indexes not there, create them
            if len(dict_list_element) - 1 < index:
                dict_list_element.extend(
                    [None for _ in range(len(dict_list_element), index + 1)],
                )

            try:
                dict_list_element[index] = set_value_from_flat_key(
                    dict_list_element[index],
                    ".".join(list_key),
                    value,
                    overwrite=overwrite,
                )
            except IndexError:
                pass

        # Other keys (dict)
        else:
            # If not dict, create one
            if not isinstance(dict_list_element, dict):
                dict_list_element = {}
            temp_dict_value = dict_list_element.get(first_key, {})

            dict_list_element[first_key] = set_value_from_flat_key(
                temp_dict_value,
                ".".join(list_key),
                value,
                overwrite=overwrite,
            )

    # If no keys left (stop condition)
    elif is_empty(flat_key):
        if not overwrite and not is_empty(dict_list_element):
            # Return current value
            return dict_list_element
        # Return new value
        return value

    # Error during split
    else:
        raise ValueError(
            "> Empty split not possible, something went wrong while setting dot dict",
        )

    # Final return to get full dict or list
    return dict_list_element


def get_nested_from_flat(
    flat_field: dict[str, Any],
    nested_field: dict | list | None = None,
) -> dict | list:
    """Generate nested json from a flatten json.

    Args:
        flat_field (dict):
            Flatten dict. int values (0, 1, 2) are considered list indexes
            Example: {'url.main': '', 'url.secondary': ''}
        nested_field (dict, optional):
            If a nested dict already exists, you might want to update it directly.
            Defaults to {}.
        TODO : Check below and set_value_from_flat_key
        # allow_override (bool, optional):
        #     If a nested field does not have "object" as value but should,
        #         it will be replace with an empty object that will be populated
        #         with other found fields
        #     Defaults to True
        #     Example: In {'url': '', 'url.main': ''} the empty value of 'url' will be
        #         replaced by an object with 'main' in it.

    Returns:
        dict:
            Nested dict.
            Example: {'url': {'main': '', 'secondary': ''}}
    """
    # Sort flatten keys
    flat_field = dict(sorted(flat_field.items()))

    # Format validation
    if nested_field is None:
        all_field_start_with_numeric = [
            re.split(r"(?<!\\)\.", key)[0].isnumeric() for key in flat_field
        ]
        if all(all_field_start_with_numeric):
            nested_field = []
        elif any(all_field_start_with_numeric):
            raise ValueError(
                "Either all fields starts with a numerical value, or none of them do",
            )
        else:
            nested_field = {}
    # Build for each field
    for key, value in flat_field.items():
        nested_field = set_value_from_flat_key(nested_field, key, value)
    return nested_field


def convert_yaml_file_to_json(yaml_path: Path) -> dict:
    """Convert a YAML file into a dict.
    The path to the YAML file is passed to the function and is loaded afterward.

    Args:
        yaml_path (Path): File path to YAML file

    Returns:
        dict: Converted YAML
    """
    with yaml_path.open(mode="r") as file:
        return yaml.safe_load(file)


def deep_merge(target_dict: dict, merge_dct: dict) -> dict:
    """Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param target_dict: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None.
    """
    for k in merge_dct:
        if (
            k in target_dict
            and isinstance(target_dict[k], dict)
            and isinstance(merge_dct[k], dict)
        ):
            deep_merge(target_dict[k], merge_dct[k])
        else:
            target_dict[k] = merge_dct[k]
