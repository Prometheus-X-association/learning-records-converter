from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


# TODO : DOCUMENTATION
# TODO : TESTING
# TODO : CHECK IF COMPLIANT IF YAML
class BasicModel(BaseModel):
    description: str = Field(
        ...,
        description="Description of the mapping.",
        examples=["Convert SCORM student ID to xAPI actor mbox"],
    )


class OutputMappingModel(BasicModel):
    output_field: str = Field(
        ..., description="Output field for the mapping.", examples=["actor.mbox"]
    )
    transformation: Union[str, List[str]] = Field(
        ...,
        description="Transformation logic.",
        examples=["lambda val: 'mailto:' + val if val else None"],
    )
    multiple: Optional[List["OutputMappingModel"]] = Field(
        ..., description="List of multiple output mapping."
    )

    # TODO : OUTPUT OR MULTIPLE


class ConditionOutputMappingModel(OutputMappingModel):
    condition: str = Field(
        ..., description="Condition for the switch.", examples=["lambda val: val == 'book'"]
    )


class CustomTransformationModel(BaseModel):
    custom: str = Field(
        ...,
        description="Custom lambda (python) code",
        examples=[
            "lambda val: 'http://example.com/xapi/verbs/completed' if val == 'completed' else None"
        ],
    )


class ValueTransformationModel(BaseModel):
    value: Any = Field(
        ..., description="Static value", examples=["http://example.com/xapi/verbs/completed"]
    )


class SwitchTransformationModel(BaseModel):
    switch: List[ConditionOutputMappingModel] = Field(
        ..., description="Static value", examples=["http://example.com/xapi/verbs/completed"]
    )


class MainMappingModel(BasicModel):
    input_fields: List[str] = Field(
        ..., description="Input field for the switch.", examples=["cmi.object.type"]
    )
    output_fields: str = Field(
        ..., description="Output field for the mapping.", examples=["actor.mbox"]
    )


class DefaultValuesModel(BasicModel):
    output_field: str = Field(
        ..., description="Output field for the default value.", examples=["datetime storage"]
    )
    value: str = Field(
        ..., description="Default value for the output field.", examples=["default_value"]
    )


class MetadataDateModel(BaseModel):
    publication: str = Field(..., description="Publication date.", examples=["2023-01-01"])
    update: str = Field(..., description="Update date.", examples=["2023-02-01"])


class MetadataModel(BasicModel):
    author: str = Field(
        ..., description="Author of the transformation config.", examples=["Your Name"]
    )
    version: float = Field(
        ..., description="Version of the transformation config.", examples=[1.0]
    )
    date: MetadataDateModel = Field(..., description="Dates related to the transformation config.")


class CompleteConfigModel(BaseModel):
    version: str = Field(..., description="Version of the transformation config.", examples=[1.0])
    input_format: str = Field(
        ..., description="Input format for the transformation.", examples=["SCORM"]
    )
    output_format: str = Field(
        ..., description="Output format for the transformation.", examples=["xAPI"]
    )
    mappings: List[MainMappingModel] = Field(..., description="List of mappings.")
    default_values: Optional[List[DefaultValuesModel]] = Field(
        ..., description="List of default values."
    )
    metadata: MetadataModel = Field(..., description="Metadata for the transformation config.")
