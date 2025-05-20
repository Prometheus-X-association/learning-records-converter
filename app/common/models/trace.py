from pydantic import BaseModel, model_validator

from app.common.common_types import JsonType
from app.common.exceptions import InvalidTraceError, UnknownFormatError
from app.common.extensions.enums import (
    CustomTraceFormatModelEnum,
    CustomTraceFormatStrEnum,
)


class Trace(BaseModel):
    """Represents a trace in a specific format.

    This class encapsulates the trace data and its associated format.
    It provides a method for automatic format detection.
    """

    data: JsonType
    format: CustomTraceFormatStrEnum
    profile: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_data_and_format(cls, values: dict) -> dict:
        """Validates the input data and format.
        If no format is provided, it attempts to detect the format automatically.

        :param values: Keyword arguments containing the trace data, format, and optional profile
        :raises InvalidTraceError: If the trace data is invalid for the specified format
        :raises UnknownFormatError: If the trace format can't be detected
        """
        input_data = values.get("data")
        input_format = values.get("format")

        if not input_data:
            raise InvalidTraceError("Trace data is required")

        if input_format:
            cls.validate_format(
                trace_data=input_data,
                trace_format=input_format,
            )
        else:
            detected_format = cls.detect_format(input_data)
            if detected_format:
                values["format"] = detected_format
            else:
                raise UnknownFormatError("Unable to detect trace format")

        return values

    @staticmethod
    def validate_format(
        trace_data: JsonType,
        trace_format: CustomTraceFormatStrEnum,
    ) -> bool:
        """Validate the input data against a specified format.

        :param trace_data: The input trace data to validate
        :param trace_format: The format to validate against

        :return: True if the data is valid for the specified format
        :raises InvalidTraceError: If the trace format is incorrect
        """
        try:
            CustomTraceFormatModelEnum[trace_format.name].value(**trace_data)
        except (ValueError, TypeError) as e:
            raise InvalidTraceError(
                f"Invalid trace for specified format: {trace_format.name}",
            ) from e
        return True

    @classmethod
    def detect_format(cls, data: JsonType) -> CustomTraceFormatStrEnum | None:
        """Attempt to detect the format of the input trace data.

        This method tries to validate the data against all known formats.

        :param data: The input trace data to analyze

        :return: The detected format, or None if no format matches
        """
        for trace_format in CustomTraceFormatStrEnum:
            if trace_format == CustomTraceFormatStrEnum.CUSTOM:
                continue
            try:
                if cls.validate_format(trace_data=data, trace_format=trace_format):
                    return trace_format
            except InvalidTraceError:
                continue
        return None
