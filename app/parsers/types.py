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
    """
    Enumeration of quoting options.

    Attributes:
        ALL (int): Quote all fields.
        MINIMAL (int): Quote fields only if they contain special characters.
        NONE (int): Never quote fields.
        NONNUMERIC (int): Quote all non-numeric fields.
    """

    ALL = csv.QUOTE_ALL
    MINIMAL = csv.QUOTE_MINIMAL
    NONE = csv.QUOTE_NONE
    NONNUMERIC = csv.QUOTE_NONNUMERIC
