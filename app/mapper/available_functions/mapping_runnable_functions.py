# Callable functions for yaml files
from os.path import join as path_join
from re import match, search
from typing import Any
from urllib.parse import urlparse

from utils.utils_dict import remove_empty_elements
from utils.utils_general import is_empty, replace_empty
