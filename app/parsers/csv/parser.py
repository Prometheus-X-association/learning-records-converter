import csv
from decimal import Decimal, InvalidOperation
from io import TextIOWrapper
from typing import Any, Iterator, OrderedDict, BinaryIO

from app.parsers.contracts.parser import Parser
from app.parsers.types import DelimiterEnum


class CSVParser(Parser):
    """
    Parser for CSV files.
    """

    def parse(self, file: BinaryIO) -> Iterator[dict[str, Any]]:
        """
        Parse the given CSV file and yield parsed rows.

        :param file: The CSV file to parse
        :yield: Parsed rows from the CSV file
        :raises ValueError: If there's an error decoding the file or parsing the CSV
        """
        try:
            text_io = TextIOWrapper(file, encoding=self.config.encoding)
            dialect = self._detect_dialect(text_io)
            reader = csv.DictReader(
                text_io, **self._get_csv_params(detected_dialect=dialect)
            )
            for row in reader:
                yield self.clean_row(row=row)

        except UnicodeDecodeError as e:
            raise ValueError(
                f"Unable to decode CSV with encoding {self.config.encoding}"
            ) from e
        except csv.Error as e:
            raise ValueError(f"CSV Parsing error: {str(e)}") from e

    @staticmethod
    def _detect_dialect(file: TextIOWrapper) -> csv.Dialect:
        """
        Detect the dialect of the CSV file.

        :param file: The CSV file
        :return: The detected CSV dialect
        """
        try:
            sample = file.read(4096)
            file.seek(0)
            return csv.Sniffer().sniff(sample, [e.value for e in DelimiterEnum])
        except csv.Error:
            return csv.excel

    def clean_row(self, row: dict) -> OrderedDict:
        """
        Clean and normalize the values in a row.

        :param row: The row to clean
        :return: The cleaned row with normalized values
        """
        return OrderedDict((k, self._normalize_value(value=v)) for k, v in row.items())

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        """
        Normalize a single value.

        :param value: The value to normalize
        :return: The normalized value
        """
        if not isinstance(value, str):
            return value
        value = value.strip()
        try:
            return Decimal(value).normalize()
        except InvalidOperation:
            return value

    def _get_csv_params(self, detected_dialect: csv.Dialect) -> dict[str, Any]:
        """
        Get CSV parameters based on the detected dialect and configuration.

        :param detected_dialect: The detected CSV dialect
        :return: CSV parameters to use for parsing
        """
        return {
            attr: getattr(self.config, attr) or getattr(detected_dialect, attr)
            for attr in [
                "delimiter",
                "quotechar",
                "escapechar",
                "doublequote",
                "skipinitialspace",
                "lineterminator",
                "quoting",
            ]
        }
