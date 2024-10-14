from extensions.enums import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum
from pydantic import BaseModel, ValidationError, model_validator
from pydantic.v1 import ValidationError as V1ValidationError

from app.common.common_types import JsonType


class Trace(BaseModel):
    """
    Represents a trace in a specific format.

    This class encapsulates the trace data and its associated format.
    It provides a method for automatic format detection.
    """

    data: JsonType
    format: CustomTraceFormatStrEnum
    profile: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_data_and_format(cls, values: dict) -> dict:
        """
        Validates the input data and format.
        If no format is provided, it attempts to detect the format automatically.

        :param data: Keyword arguments containing the trace data, format, and optional profile
        :raises ValueError: If the trace data is invalid for the specified format
        """
        input_data = values.get("data")
        input_format = values.get("format")

        if not input_data:
            raise ValueError("Input trace data is required")

        if input_format:
            if not cls.validate_format(trace_data=input_data, trace_format=input_format):
                raise ValueError(f"Invalid trace for specified format: {input_format}")
        else:
            detected_format = cls.detect_format(input_data)
            if detected_format:
                values["format"] = detected_format
            else:
                raise ValueError("Unable to detect trace format")

        return values

    @staticmethod
    def validate_format(trace_data: JsonType, trace_format: CustomTraceFormatStrEnum) -> bool:
        """
        Validate the input data against a specified format.

        :param trace_data: The input trace data to validate
        :param trace_format: The format to validate against

        :return: True if the data is valid for the specified format, False otherwise
        """
        try:
            CustomTraceFormatModelEnum[trace_format.name].value(**trace_data)
        except (ValidationError, V1ValidationError):
            return False
        return True

    @classmethod
    def detect_format(cls, data: JsonType) -> CustomTraceFormatStrEnum | None:
        """
        Attempt to detect the format of the input trace data.

        This method tries to validate the data against all known formats.

        :param data: The input trace data to analyze

        :return: The detected format, or None if no format matches
        """
        for trace_format in CustomTraceFormatStrEnum:
            if trace_format == CustomTraceFormatStrEnum.CUSTOM:
                continue
            if cls.validate_format(trace_data=data, trace_format=trace_format):
                return trace_format
        return None
