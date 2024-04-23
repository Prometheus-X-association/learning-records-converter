from typing import Optional

from enums.custom_trace_format import CustomTraceFormatStrEnum
from pydantic import BaseModel, Field


class TransformInputTraceRequestModel(BaseModel):
    input_format: CustomTraceFormatStrEnum = Field(default=None, description="Input trace format")
    output_format: CustomTraceFormatStrEnum = Field(default=CustomTraceFormatStrEnum.XAPI, description="Output trace format")  # type: ignore
    input_trace: dict = Field(description="Input trace to convert in JSON format")


class TransformInputTraceResponseModel(BaseModel):
    output_trace: dict = Field(description="Transformed output trace in JSON format")


class ValidateInputTraceRequestModel(BaseModel):
    input_format: CustomTraceFormatStrEnum = Field(default=None, description="Input trace format")
    # input_format: CustomTraceFormatStrEnum = Field(description="Input trace format")
    input_trace: dict = Field(description="Input trace to convert in JSON format")


class ValidateInputTraceResponseModel(BaseModel):
    input_format: CustomTraceFormatStrEnum = Field(description="Input trace format.")
