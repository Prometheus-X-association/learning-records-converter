from typing import Any

from enums.custom_trace_format import CustomTraceFormatStrEnum
from pydantic import BaseModel, Field

from app.common.models.trace import Trace
from app.profile_enricher.types import ValidationRecommendation


class InputTraceRequestModel(BaseModel):
    input_trace: dict[str, Any]
    input_format: CustomTraceFormatStrEnum = Field(
        default=None, description="Input trace format"
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
        else:
            return Trace.create_with_format_detection(data=self.input_trace)


# Transformation models
class TransformInputTraceRequestModel(InputTraceRequestModel):
    output_format: CustomTraceFormatStrEnum = Field(
        default=CustomTraceFormatStrEnum.XAPI, description="Output trace format"
    )


class TransformInputTraceResponseMetaModel(BaseModel):
    input_format: CustomTraceFormatStrEnum = Field(description="Input trace format")
    recommendations: list[ValidationRecommendation] = Field(
        default_factory=list,
        description="List of recommendations to improve output trace",
    )


class TransformInputTraceResponseModel(BaseModel):
    output_trace: dict[str, Any] = Field(
        description="Transformed output trace in JSON format"
    )
    meta: TransformInputTraceResponseMetaModel


# Validation models
class ValidateInputTraceRequestModel(InputTraceRequestModel):
    pass


class ValidateInputTraceResponseModel(BaseModel):
    input_format: CustomTraceFormatStrEnum = Field(description="Input trace format.")
