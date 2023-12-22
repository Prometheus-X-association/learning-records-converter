from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, model_validator


# TODO : DOCUMENTATION
# TODO : TESTING
# TODO : CHECK IF COMPLIANT IF YAML
class BasicModel(BaseModel):
    description: Optional[str] = Field(
        default=None,
        description="Description of the mapping.",
        examples=["Convert SCORM student ID to xAPI actor mbox"],
    )


class BasicTransformationModel(BaseModel):
    pass


class CustomTransformationModel(BasicTransformationModel):
    custom: List[str] = Field(
        ...,
        description="List of custom lambda (python) code?",
        examples=[
            "lambda val: 'http://example.com/xapi/verbs/completed' if val == 'completed' else None"
        ],
    )


class ValueTransformationModel(BasicTransformationModel):
    value: Any = Field(
        ..., description="Static value", examples=["http://example.com/xapi/verbs/completed"]
    )


class OutputMappingModel(BasicModel):
    output_field: Optional[str] = Field(
        default=None, description="Output field for the mapping.", examples=["actor.mbox"]
    )
    transformation: Optional[
        Union["CustomTransformationModel", "ValueTransformationModel", "SwitchTransformationModel"]
    ] = Field(default=None, description="Transformation logic.")

    multiple: Optional[List["OutputMappingModel"]] = Field(
        default=[], description="List of multiple output mapping."
    )

    @model_validator(mode="before")
    def validate_output_field_transformation_xor_multiple(cls, values):
        output_field, transformation, multiple = (
            values.get("output_field"),
            values.get("transformation"),
            values.get("multiple"),
        )
        if (output_field or transformation) and multiple:
            raise ValueError(
                "Either 'output_field' and 'transformation' or 'multiple' should be provided, not both."
            )
        if not (output_field or transformation) and not multiple:
            raise ValueError(
                "Either 'output_field' and 'transformation' or 'multiple' should be provided."
            )

        return values


class ConditionOutputMappingModel(OutputMappingModel):
    condition: str = Field(
        ..., description="Condition for the switch.", examples=["lambda val: val == 'book'"]
    )

    @model_validator(mode="before")
    def validate_output_field_transformation(cls, values):
        output_field, transformation, multiple = (
            values.get("output_field"),
            values.get("transformation"),
            values.get("multiple"),
        )
        if transformation and not output_field:
            raise ValueError(
                "If 'transformation' is defined, 'output_field' also needs to be define."
            )

        return values


class SwitchTransformationModel(BasicTransformationModel):
    switch: List[ConditionOutputMappingModel] = Field(
        ..., description="Static value", examples=["http://example.com/xapi/verbs/completed"]
    )


class MainMappingModel(BasicModel):
    input_fields: List[str] = Field(
        ..., description="Input field for the switch.", examples=["cmi.object.type"]
    )
    output_fields: OutputMappingModel = Field(..., description="Output field for the mapping.")


class MetadataDateModel(BaseModel):
    publication: str = Field(..., description="Publication date.", examples=["2023-01-01"])
    update: str = Field(..., description="Update date.", examples=["2023-02-01"])


class MetadataModel(BasicModel):
    author: str = Field(
        ..., description="Author of the transformation config.", examples=["Your Name"]
    )
    # version: float = Field(
    #     ..., description="Version of the transformation config.", examples=[1.0]
    # )
    date: MetadataDateModel = Field(..., description="Dates related to the transformation config.")


class CompleteConfigModel(BaseModel):
    version: float = Field(
        ..., description="Version of the transformation config.", examples=[1.0]
    )
    input_format: str = Field(
        ..., description="Input format for the transformation.", examples=["SCORM"]
    )
    output_format: str = Field(
        ..., description="Output format for the transformation.", examples=["xAPI"]
    )
    mappings: List[MainMappingModel] = Field(..., description="List of mappings.")
    default_values: List[OutputMappingModel] = Field(
        default=[], description="List of default values."
    )
    metadata: MetadataModel = Field(..., description="Metadata for the transformation config.")
