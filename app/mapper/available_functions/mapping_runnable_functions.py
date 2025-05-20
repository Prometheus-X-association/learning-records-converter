# Callable functions for yaml files
from collections.abc import Callable
from os.path import join as path_join
from re import match, search
from urllib.parse import urlparse

from utils.utils_date import parse_date
from utils.utils_general import is_empty


def get_available_functions() -> dict[str, Callable]:
    """Returns a list of functions available in mapping trace formats."""
    return {
        "is_empty": is_empty,
        "match": match,
        "parse_date": parse_date,
        "path_join": path_join,
        "search": search,
        "urlparse": urlparse,
    }
