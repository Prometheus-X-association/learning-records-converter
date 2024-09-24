from extensions.enums import CustomTraceFormatStrEnum
from pydantic import BaseModel, Field

from app.common.common_types import JsonType
from app.common.models.trace import Trace
from app.parsers.types import DelimiterEnum, QuotingEnum
from app.profile_enricher.profiler_types import ValidationRecommendation

DEFAULT_OUTPUT_FORMAT = CustomTraceFormatStrEnum.XAPI


class InputTraceRequestModel(BaseModel):
    """Model for input trace request."""

    input_trace: JsonType = Field(..., description="Input trace data")
    input_format: CustomTraceFormatStrEnum | None = Field(
        default=None,
        description="Input trace format",
    )

    def get_trace(self) -> Trace:
        """
        Create a Trace instance from the input data.

        If an input_format is provided, it uses that format.
        Otherwise, it attempts to detect the format automatically.

        :return: A new Trace instance created from the input data
        :raises ValueError: If the trace format is not provided and cannot be detected
        """
        if self.input_format:
            return Trace(data=self.input_trace, format=self.input_format)
        return Trace.create_with_format_detection(data=self.input_trace)


# Transformation models
class TransformInputTraceRequestModel(InputTraceRequestModel):
    """Model for transform input trace request."""

    output_format: CustomTraceFormatStrEnum = Field(
        default=DEFAULT_OUTPUT_FORMAT,
        description="Output trace format",
    )


class TransformInputTraceResponseMetaModel(BaseModel):
    """Model for transform input trace response metadata."""

    input_format: CustomTraceFormatStrEnum = Field(description="Input trace format")
    recommendations: list[ValidationRecommendation] = Field(
        default_factory=list,
        description="List of recommendations to improve output trace",
    )


class TransformInputTraceResponseModel(BaseModel):
    """Model for transform input trace response."""

    output_trace: JsonType = Field(
        description="Transformed output trace in JSON format",
    )
    meta: TransformInputTraceResponseMetaModel


# Validation models
class ValidateInputTraceRequestModel(InputTraceRequestModel):
    """Model for validate input trace request."""


class ValidateInputTraceResponseModel(BaseModel):
    """Model for validate input trace response."""

    input_format: CustomTraceFormatStrEnum = Field(description="Input trace format.")


# Custom file transformation models
class CustomConfigModel(BaseModel):
    encoding: str | None = Field(
        default="utf-8",
        description="Encoding of the file",
    )
    delimiter: DelimiterEnum | None = Field(
        default=None,
        description="Separator used in the file, if applicable",
    )
    quotechar: str | None = Field(
        default=None,
        description="Character used to quote fields",
    )
    escapechar: str | None = Field(
        default=None,
        description="Character used to escape special characters",
    )
    doublequote: bool | None = Field(
        default=None,
        description="Whether to double quote characters within quoted fields",
    )
    skipinitialspace: bool | None = Field(
        default=None,
        description="Whether to skip initial spaces in fields",
    )
    lineterminator: str | None = Field(
        default=None,
        description="Character(s) used to terminate lines",
    )
    quoting: QuotingEnum | None = Field(
        default=None,
        description="Quoting style used in the CSV file",
    )
