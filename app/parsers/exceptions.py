class ParserError(Exception):
    """Base exception for parser exceptions."""


class ParserFactoryError(Exception):
    """Exception raised for errors in the ParserFactory."""


class CSVParsingError(ParserError):
    """Exception raised for errors during CSV parsing."""


class InvalidCSVStructureError(CSVParsingError):
    """Exception raised when the CSV structure is invalid (e.g., no header or single column)."""
