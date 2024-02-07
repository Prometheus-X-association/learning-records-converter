from enums import CustomTraceFormatModelEnum
from pydantic import ValidationError
from pydantic.v1 import ValidationError as ValidationErrorV1


def get_format_from_trace(trace: dict) -> CustomTraceFormatModelEnum | None:
    """Try to determine the trace format from the trace itself.

    Args:
        trace (dict): Trace

    Returns:
        CustomTraceFormatModelEnum | None: Format corresponding to trace or None if nothing is found.
    """
    for format in CustomTraceFormatModelEnum:
        try:
            format.value(**trace)
            return format
        except (ValidationError, ValidationErrorV1) as ve:
            pass
