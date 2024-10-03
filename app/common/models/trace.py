from extensions.enums import CustomTraceFormatModelEnum, CustomTraceFormatStrEnum
from pydantic import BaseModel, ValidationError
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

    def __init__(self, **data):
        """
        Initialize a new Trace instance.

        :param data: Keyword arguments containing the trace data, format, and optional profile
        :raises ValueError: If the trace data is invalid for the specified format
        """
        super().__init__(**data)
        self._validate_trace()

    def _validate_trace(self) -> None:
        """
        Validate the trace data against its specified format.

        :raises ValueError: If the trace data is invalid for the specified format
        """
        format_model = CustomTraceFormatModelEnum[self.format.name]
        try:
            format_model.value(**self.data)
        except (ValidationError, V1ValidationError) as e:
            raise ValueError("Invalid trace") from e

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
            if trace_format == CustomTraceFormatModelEnum.CUSTOM:
                continue
            try:
                trace_format.value(**data)
                return cls(
                    data=data,
                    format=CustomTraceFormatStrEnum[trace_format.name],
                )
            except (ValidationError, V1ValidationError):
                continue
        raise ValueError("Unable to detect trace format")
