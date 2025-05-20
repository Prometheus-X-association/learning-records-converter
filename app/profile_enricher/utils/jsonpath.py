from collections.abc import Mapping
from functools import cache
from typing import Any

import jsonpath_ng


class JSONPathUtils:
    """Utility class responsible for handling JSONPath data."""

    @staticmethod
    @cache
    def parse_jsonpath(path: str) -> jsonpath_ng.JSONPath:
        """Parse and cache a JSONPath expression.

        :param path: The JSONPath expression to parse
        :return: Parsed JSONPath object
        :raises ValueError: If the JSONPath is invalid
        """
        try:
            return jsonpath_ng.parse(path)
        except Exception as e:
            raise ValueError(f"Invalid JSONPath: {path}") from e

    @staticmethod
    def path_exists(path: str, data: Mapping[str, Any]) -> bool:
        """Check if a value exists at the specified JSONPath.

        :param data: The data to check
        :param path: The JSONPath expression
        :return: True if a value exists, False otherwise
        """
        return bool(JSONPathUtils.parse_jsonpath(path).find(data))

    @staticmethod
    def path_to_dict(path: str, value: str) -> dict[str, Any]:
        """Transform a jsonpath to a dict with the passed value.

        :param path: The JSON path
        :param value: The value to be set at the specified path
        :return: A dictionary representing the transformed rule
        """
        # Remove the initial '$.' if present
        path = path.removeprefix("$.")

        # Split the main path and the part in brackets
        # Example : $.object.definition.extensions['https://w3id.org/xapi/acrossx/extensions/type']
        if "[" in path and "]" in path:
            main_path, extension = path.split("[", 1)
            extension = extension.strip("']")
            return {main_path: {extension: value}}

        # If there's no part in brackets, set the value directly
        return {path: value}
