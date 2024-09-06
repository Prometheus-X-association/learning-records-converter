from typing import Optional

from extensions.enums import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum
from pydantic import BaseModel, ValidationError
from pydantic.v1 import ValidationError as V1ValidationError

from app.common.type.types import JsonType


class Trace(BaseModel):
    """
    Represents a trace in a specific format.

    This class encapsulates the trace data and its associated format.
    It provides a method for automatic format detection.

    :param data: The raw trace data
    :param format: The format of the trace
    :param profile: The profile associated with this trace, if any
    """

    data: JsonType
    format: CustomTraceFormatStrEnum
    profile: Optional[str] = None

    @classmethod
    def create_with_format_detection(cls, data: JsonType) -> "Trace":
        """
        Create a Trace instance with automatic format detection.

        This method attempts to detect the format of the trace by validating
        it against known formats.

        :param data: The raw trace data
        :return: A new Trace instance with the detected format
        :raises ValueError: If the trace format cannot be detected
        """
        for trace_format in CustomTraceFormatModelEnum:
            try:
                trace_format.value(**data)
                return cls(
                    data=data, format=CustomTraceFormatStrEnum[trace_format.name]
                )
            except (ValidationError, V1ValidationError):
                continue
        raise ValueError("Unable to detect trace format")
