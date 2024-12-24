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
    """Get value from a dict element by using a flatten key (keys separated with dotes).

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
    # Split the flat_key, but keep keys with brackets intact
    keys = re.split(r"\.(?![^\[]*\])", flat_key)

    # Error during split
    if not keys:
        raise ValueError(
            "> Empty split not possible, something went wrong while setting dot dict",
        )

    # If flat_key is empty, return the value or the original dict_list_element based on overwrite
    if is_empty(flat_key):
        return value if overwrite else dict_list_element

    # Handle the case where dict_list_element is empty and overwrite is False
    if not dict_list_element and not overwrite:
        return dict_list_element

    current = dict_list_element
    for i, full_key in enumerate(keys):
        # Handle keys with brackets (e.g., for extensions)
        match = re.match(r"(.+?)\[(.+)\]", full_key)
        if match:
            key, subkey = match.group(1), match.group(2).strip("'\"")
        else:
            key, subkey = full_key.replace(r"\.", "."), None

        try:
            # Handle numeric keys for list indexing
            if key.isnumeric():
                key = int(key)
                if not isinstance(current, list):
                    current = []
                    if i == 0:
                        dict_list_element = current
                # Extend the list if the index is out of range
                while len(current) <= key:
                    current.append(None)

            if i == len(keys) - 1:
                # We've reached the final key
                if subkey:
                    # Handle extension-like keys
                    if not isinstance(current, dict):
                        current = {}
                        if i == 0:
                            dict_list_element = current
                    current.setdefault(key, {})
                    if (
                        overwrite
                        or subkey not in current[key]
                        or is_empty(current[key][subkey])
                    ):
                        current[key][subkey] = value
                elif overwrite or key not in current or is_empty(current[key]):
                    current[key] = value
            elif subkey:
                # Handle extension-like keys
                if not isinstance(current, dict):
                    current = {}
                    if i == 0:
                        dict_list_element = current
                current.setdefault(key, {}).setdefault(subkey, {})
                current = current[key][subkey]
            else:
                # Determine if the next key is numeric (for list creation)
                next_key_is_numeric = (
                    keys[i + 1].isnumeric() if i + 1 < len(keys) else False
                )
                if isinstance(current, list):
                    if current[key] is None:
                        current[key] = [] if next_key_is_numeric else {}
                else:
                    if not isinstance(current, dict):
                        current = {}
                        if i == 0:
                            dict_list_element = current
                    if key not in current or not isinstance(
                        current[key],
                        dict | list,
                    ):
                        current[key] = [] if next_key_is_numeric else {}
                current = current[key]
        except IndexError:
            pass

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


def deep_merge(target_dict: dict, merge_dct: dict) -> None:
    """Recursive dict merge.

    Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into ``target_dict``.

    :param target_dict: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None.
    """
    for key, value in merge_dct.items():
        target_value = target_dict.get(key)

        # If both target and merge values are dictionaries, merge recursively
        if isinstance(target_value, dict) and isinstance(value, dict):
            deep_merge(target_value, value)
        # If both are sets, perform union
        elif isinstance(target_value, set) and isinstance(value, set):
            target_value.update(value)
        # If target is a list and merge value is a list, extend it
        elif isinstance(target_value, list) and isinstance(value, list):
            target_value.extend(value)
        # If target is a list and merge value is not a list, append to the list
        elif isinstance(target_value, list):
            target_value.append(value)
        # If target is a dictionary but merge value is a list, wrap target in a list
        elif isinstance(target_value, dict) and isinstance(value, list):
            target_dict[key] = [target_value, *value]
        # Handle cases where one value is None: keep the non-None value
        elif target_value is None:
            target_dict[key] = value
        elif value is None:
            continue  # Keep the target value unchanged if the merge value is None
        # In all other cases, replace the target value with the merge value
        else:
            target_dict[key] = value
