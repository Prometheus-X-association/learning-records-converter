import csv
from collections import OrderedDict
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from io import TextIOWrapper
from typing import Any, BinaryIO

from app.common.extensions.enums import CustomTraceFormatStrEnum
from app.common.models.trace import Trace
from app.parsers.contracts.parser import Parser
from app.parsers.exceptions import CSVParsingError, InvalidCSVStructureError
from app.parsers.types import DelimiterEnum


class CSVParser(Parser):
    """
    Parser for CSV files.
    """

    def parse(self, file: BinaryIO) -> Iterator[Trace]:
        """
        Parse the given CSV file and yield parsed rows.

        :param file: The CSV file to parse
        :yield: Parsed rows from the CSV file
        :raises CSVParsingError: If there's an error decoding the file or parsing the CSV
        """
        self.logger.info("Parsing start", {"config": self.parsing_config.model_dump()})

        text_io = self._open_file(file=file)
        dialect, has_header = self._detect_csv_properties(file=text_io)
        self.logger.debug("Detected dialect", {"dialect": dialect.__dict__})

        reader = self._create_csv_reader(file=text_io, dialect=dialect)
        self._validate_csv_structure(reader=reader, file=text_io, has_header=has_header)

        for row in reader:
            yield Trace(
                data=self._clean_row(row=row),
                format=CustomTraceFormatStrEnum.CUSTOM,
            )

        self.logger.info("Parsing end", {"config": self.parsing_config.model_dump()})

    def _open_file(self, file: BinaryIO) -> TextIOWrapper:
        """
        Open the binary file as a text file with the specified encoding.

        :param file: The binary file to open
        :return: A TextIOWrapper object
        :raises CSVParsingError: If there's an error decoding the file
        """
        try:
            return TextIOWrapper(buffer=file, encoding=self.parsing_config.encoding)
        except UnicodeDecodeError as e:
            msg = "Unable to decode CSV"
            self.logger.exception(msg, e, {"encoding": self.parsing_config.encoding})
            raise CSVParsingError(msg) from e

    def _detect_csv_properties(self, file: TextIOWrapper) -> tuple[csv.Dialect, bool]:
        """
        Detect CSV dialect and presence of a header.

        :param file: The CSV file
        :return: Tuple of (detected dialect, has_header)
        """
        try:
            sample = file.read(4096)
            file.seek(0)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(
                sample=sample,
                delimiters=[e.value for e in DelimiterEnum],
            )
            has_header = sniffer.has_header(sample=sample)
            return dialect, has_header
        except csv.Error:
            self.logger.warning("Unable to detect CSV dialect, falling back to excel")
            return csv.excel, True

    def _create_csv_reader(
        self,
        file: TextIOWrapper,
        dialect: csv.Dialect,
    ) -> csv.DictReader:
        """
        Create a CSV DictReader with the detected dialect and configuration.

        :param file: The CSV file
        :param dialect: The detected CSV dialect
        :return: A csv.DictReader object
        :raises CSVParsingError: If there's an error creating the CSV reader
        """
        params = self._get_csv_params(detected_dialect=dialect)
        try:
            return csv.DictReader(
                f=file,
                **params,
            )
        except csv.Error as e:
            msg = "Error creating CSV reader"
            self.logger.exception(msg, e, {"params": params})
            raise CSVParsingError(msg) from e

    @staticmethod
    def _clean_row(row: dict) -> OrderedDict:
        """
        Clean and normalize the values in a row.

        :param row: The row to clean
        :return: The cleaned row with normalized values
        """
        return OrderedDict(
            (k, CSVParser._normalize_value(value=v)) for k, v in row.items()
        )

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        """
        Normalize a single value.

        :param value: The value to normalize
        :return: The normalized value
        """
        # If the value is not a string, return it as is
        if not isinstance(value, str):
            return value

        # Remove leading and trailing whitespace
        value = value.strip()

        # Convert empty strings to None (to have null in JSON)
        if not value:
            return None

        try:
            # Attempt to convert the string to a Decimal and normalize it
            # This will remove trailing zeros and convert scientific notation to standard notation
            # With CustomJSONEncoder this allows the value to be serialized as a number in JSON
            return Decimal(value).normalize()
        except InvalidOperation:
            # If the string can't be converted to a Decimal, return the original stripped string
            return value

    def _get_csv_params(self, detected_dialect: csv.Dialect) -> dict[str, Any]:
        """
        Get CSV parameters based on the detected dialect and configuration.

        :param detected_dialect: The detected CSV dialect
        :return: CSV parameters to use for parsing
        """
        return {
            attr: getattr(self.parsing_config, attr) or getattr(detected_dialect, attr)
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

    def _validate_csv_structure(
        self, reader: csv.DictReader, file: TextIOWrapper, has_header: bool
    ) -> None:
        """
        Validate the structure of the CSV file.

        :param reader: The CSV DictReader
        :param has_header: Whether the CSV has a header
        :raises InvalidCSVStructureError: If the CSV structure is invalid
        """
        if not has_header:
            self.logger.error("CSV file has no header")
            raise InvalidCSVStructureError("CSV file must have a header row")

        first_row = next(reader.reader, None)
        if first_row is None or len(first_row) <= 1:
            self.logger.error("CSV file has only one column or is empty")
            raise InvalidCSVStructureError("CSV file must have more than one column")
        file.seek(0)
