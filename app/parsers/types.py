import csv
from enum import Enum, StrEnum


class DelimiterEnum(StrEnum):
    """
    Enumeration of possible delimiters.
    """

    COLON = ":"
    COMMA = ","
    PIPE = "|"
    SEMICOLON = ";"
    SPACE = " "
    TAB = "\t"


class QuotingEnum(Enum):
    ALL = csv.QUOTE_ALL
    MINIMAL = csv.QUOTE_MINIMAL
    NONE = csv.QUOTE_NONE
    NONNUMERIC = csv.QUOTE_NONNUMERIC
