from enum import StrEnum


class DelimiterEnum(StrEnum):
    """
    Enumeration of possible CSV delimiters.
    """
    COMMA = ","
    SEMICOLON = ";"
    TAB = "\t"
    PIPE = "|"
    SPACE = " "
    COLON = ":"
