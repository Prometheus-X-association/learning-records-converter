import re
from typing import Any, Dict, List, Tuple, Union, overload

import yaml
from utils.utils_general import is_empty


def get_flat_from_nested(
    nested_content: dict, flat_non_nested_list: bool = True, flat_nested_list: bool = True
) -> dict:
    """Generate flatten json from a nested json

    Args:
        nested_content (dict):
            Nested dict.
            Example: {'url': {'main': '', 'secondary': [1, 2]}}
        flat_non_nested_list (bool):
            Also flat non nested list element.
            Example:
                if True, {'url': [1, 2]} becomes {"url.0": 1, "url.1": 2}
                else, {'url': [1, 2]} becomes {'url': [1, 2]}
            Default value is True.

    Returns:
        dict: Flatten dict
            Example: {'url.main': '', 'url.secondary.0': 1, 'url.secondary.1': 2}}
    """

    flatten_field = {}

    def recursive_flat_from_nested(content, field_name=""):
        # If dict type
        if isinstance(content, dict) and content:
            for key in content:
                key_encoded = key.replace(".", "\.")
                recursive_flat_from_nested(content[key], field_name + key_encoded + ".")

        # If list type
        elif isinstance(content, list) and content:
            list_element_nested = [isinstance(element, (list, dict)) for element in content]

            if (
                (flat_nested_list and flat_non_nested_list)
                or (flat_nested_list and any(list_element_nested))
                or (flat_non_nested_list and not all(list_element_nested))
            ):
                for index, value in enumerate(content):
                    recursive_flat_from_nested(value, field_name + str(index) + ".")
            else:
                flatten_field[field_name[:-1]] = content

        # Final value
        else:
            flatten_field[field_name[:-1]] = content

    recursive_flat_from_nested(nested_content)
    return flatten_field


@overload
def remove_empty_elements(dictionnary: list) -> list: ...


@overload
def remove_empty_elements(dictionnary: dict) -> dict: ...


def remove_empty_elements(dictionnary: Union[list, dict]) -> Union[list, dict]:
    """Remove empty fields

    Args:
        dictionnary : dictionnary to remove empty fields

    Returns:
        dictionnary with removed fields
    """
    if not isinstance(dictionnary, (dict, list)):
        return dictionnary
    elif isinstance(dictionnary, list):
        return [
            value
            for value in (remove_empty_elements(value) for value in dictionnary)
            if not is_empty(value)
        ]
    else:
        return {
            key: value
            for key, value in (
                (key, remove_empty_elements(value)) for key, value in dictionnary.items()
            )
            if not is_empty(value)
        }


def get_value_from_flat_key(
    dict_element: Union[dict, list], flat_key: str, default_value=None, return_copy=True
) -> Any:
    """Get value from a dict element by using a flatten key (keys seperated with dotes)
    If the value exists (even if it's empty), the method returns the value.
    Else, the 'default_value' is returned

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
            except IndexError as ie:
                print("out of index in list:", ie)
                value = default_value
        elif not key.isnumeric() and isinstance(value, dict):
            value = value.get(key, default_value)
        else:
            value = default_value
        if not value:
            if index < total_list_key_len:
                value = default_value
            break
    if return_copy and isinstance(value, (list, dict)):
        return value.copy()
    else:
        return value


@overload
def set_value_from_flat_key(
    dict_list_element: dict, flat_key: str, value: Any, overwrite: bool = True
) -> dict: ...


@overload
def set_value_from_flat_key(
    dict_list_element: list, flat_key: str, value: Any, overwrite: bool = True
) -> list: ...


def set_value_from_flat_key(
    dict_list_element: Union[dict, list],
    flat_key: str,
    value: Any,
    overwrite: bool = True,
) -> Union[dict, list]:
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
        first_key = first_key.replace("\.", ".")

        # If not overwrite but found element is not list, dict or None, return
        if (
            not overwrite
            and not (isinstance(dict_list_element, list) or isinstance(dict_list_element, dict))
            and not is_empty(dict_list_element)  # before : None
        ):
            print("> Warning - an item already have value and behavior is : NOT overwriting")
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
                dict_list_element.extend([None for i in range(len(dict_list_element), index + 1)])

            try:
                dict_list_element[index] = set_value_from_flat_key(
                    dict_list_element[index],
                    ".".join(list_key),
                    value,
                    overwrite=overwrite,
                )
            except IndexError as ie:
                print("IndexError :", ie)

        # Other keys (dict)
        else:
            # If not dict, create one
            if not isinstance(dict_list_element, dict):
                dict_list_element = {}
            temp_dict_value = dict_list_element.get(first_key, {})

            dict_list_element[first_key] = set_value_from_flat_key(
                temp_dict_value, ".".join(list_key), value, overwrite=overwrite
            )

    # If no keys left (stop condition)
    elif is_empty(flat_key):
        if not overwrite and not is_empty(dict_list_element):
            print(
                "> Warning - dict_list_element already have value and behavior is : NOT overwriting"
            )
            # Return current value
            return dict_list_element
        else:
            # Return new value
            return value

    # Error during split
    else:
        raise ValueError("> Empty split not possible, something went wrong while setting dot dict")

    # Final return to get full dict or list
    return dict_list_element


def get_nested_from_flat(
    flat_field: Dict[str, Any], nested_field: Union[dict, list, None] = None
) -> Union[dict, list]:
    """Generate nested json from a flatten json

    Args:
        flat_field (dict):
            Flatten dict. int values (0, 1, 2) are concidered list indexes
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
            re.split(r"(?<!\\)\.", key)[0].isnumeric() for key in flat_field.keys()
        ]
        if all(all_field_start_with_numeric):
            nested_field = []
        elif any(all_field_start_with_numeric):
            raise ValueError("Either all fields starts with a numerical value, or none of them do")
        else:
            nested_field = {}
    # Build for each field
    for key, value in flat_field.items():
        nested_field = set_value_from_flat_key(nested_field, key, value)
    return nested_field


def drop_duplicates_in_list_on_field(
    list_dict_content: list, list_field: list, keep_first: bool = True
) -> list:
    """Drop duplicates in a list of dicts based on one or several fields.

    The key in a dictionnary is unique. This algorithme is based on that rule.
    We create a temporary dictionnary where the key is the concatination of all fields values,
    and the value is the dictionnary itself.

    We then get all values in order to get only single occurence of
    a dictionnary depending on specific fields.

    CAUTION:
        If an undefied field is passed, no error will be raised.
        It will be considered to have a "None" value

    TODO:
        Keep first, or keep last param? default keep last

    Args:
        list_dict_content (list): list of dictionnary to drop duplilcate on
        list_field (list): list of fields (string) to base unicity on.
            Fields can be nested by using the "dot syntax" (field_a.field_b)
        keep_first (bool): Keep first occurence (True) or last (False). Default value : True

    Returns:
        list: list of unique dictionnary
    """
    dict_temp = {}
    for dict_content in list_dict_content:
        new_key = "_".join(
            [str(get_value_from_flat_key(dict_content, field)) for field in list_field]
        )
        if not keep_first or new_key not in dict_temp:
            dict_temp[new_key] = dict_content

    return list(dict_temp.values())


def is_flat_key_in_dict(list_dict_content: Union[dict, list], flat_key: str) -> bool:
    """Check if a flatten key is in a nested element

    Args:
        list_dict_content (Union[dict, list]): element to search in
        flat_key (str): concerned key

    Returns:
        bool: If key is found return True, else False
    """
    list_split_key = flat_key.split(".")
    for key in list_split_key:
        # Index and List
        if key.isnumeric() and isinstance(list_dict_content, list):
            try:
                list_dict_content = list_dict_content[int(key)]
            except IndexError as ie:
                return False
        # Key and Dict
        elif not key.isnumeric() and isinstance(list_dict_content, dict):
            try:
                list_dict_content = list_dict_content[key]
            except KeyError as ke:
                return False
        # None of the above
        else:
            return False
    return True


def get_value_from_first_key_available(
    json_element: dict, base_field: str, keys_tuple: Union[Tuple[str, ...], List[str]]
) -> Tuple[Any, str]:
    """
    Get the first non empty field subvalue of a dict element,
    based on a tuple of subfields to check,
    and the chosen key that leads to this value.

    Ex: base_field = "department" / keys_tuple = ("code", "base")
    department.code is returned if not empty, else department.base

    If all values are empty, ("", "") is returned.

    Args:
        json_element (dict): Full dict with data.
        base_field (str): Name of the main field.
            If "", will look up for fields in keys_tuple directly.
        keys_tuple (Union[Tuple[str], List[str]]): Tuple of subfields to check.
            A list of subfields is also allowed.

    Returns:
        Tuple[Any, str]: Tuple based on (value, key) with :
            value = Dict value if not empty, else "".
            key = base_field with the chosen key added if possible, else "".
    """
    value = ""
    current_key = ""

    if isinstance(json_element, dict) and isinstance(keys_tuple, (tuple, list)):
        if isinstance(base_field, str):
            if not is_empty(base_field):
                base_field += "."
        else:
            # Allow "" to loop only over fields in keys_tuple
            base_field = ""

        for key in keys_tuple:
            # Sanitize 'key' entry
            if is_empty(key):
                key = ""
            else:
                key = str(key)

            current_key = base_field + key
            value = get_value_from_flat_key(json_element, current_key, default_value="")
            if not is_empty(value):
                # Return value and chosen key
                return value, current_key
            else:
                # Reaffect default values
                current_key = ""
                value = ""
    return value, current_key


def convert_yaml_file_to_json(yaml_path: str) -> dict:
    """Convert a YAML file into a dict.
    The path to the YAML file is passed to the function and is loaded afterwards

    Args:
        yaml_path (str): File path to YAML file

    Raises:
        ValueError: empty path

    Returns:
        dict: Converted YAML
    """
    if yaml_path:
        with open(yaml_path, "r") as file:
            return yaml.safe_load(file)
    else:
        raise ValueError("'yaml_path' cannot be empty")
