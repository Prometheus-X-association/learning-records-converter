from typing import Any

from pydantic import BaseModel, Field, model_validator


class BasicModel(BaseModel):
    description: str | None = Field(
        default=None,
        description="Description of the mapping.",
        examples=["Convert SCORM student ID to xAPI actor mbox"],
    )


class OutputMappingModel(BasicModel):
    output_field: str | None = Field(
        default=None,
        description="Output field for the mapping.",
        examples=["actor.mbox"],
    )

    value: Any | None = Field(
        default=None,
        description="Static value",
        examples=["http://example.com/xapi/verbs/completed"],
    )

    custom: list[str] | None = Field(
        default=None,
        description="list of custom lambda (python) code?",
        examples=[
            "lambda val: 'http://example.com/xapi/verbs/completed' if val == 'completed' else None",
        ],
    )

    switch: list["ConditionOutputMappingModel"] | None = Field(
        default=None,
        description="Static value",
        examples=["http://example.com/xapi/verbs/completed"],
    )

    multiple: list["OutputMappingModel"] | None = Field(
        default=[],
        description="list of multiple output mapping.",
    )

    profile: str | None = Field(
        default=None,
        description="Dases profile to apply.",
    )

    @model_validator(mode="before")
    @staticmethod
    def validate_output_field_transformation_xor_multiple(values):
        output_field, value, custom, switch, multiple, profile = (
            values.get("output_field"),
            values.get("value"),
            values.get("custom"),
            values.get("switch"),
            values.get("multiple"),
            values.get("profile"),
        )
        if (output_field or value or custom or switch) and multiple:
            raise ValueError("Only one mapping should be provided.")
        if not (output_field or value or custom or switch or profile or multiple):
            raise ValueError("A mapping should be provided.")

        return values


class ConditionOutputMappingModel(OutputMappingModel):
    condition: str = Field(
        ...,
        description="Condition for the switch.",
        examples=["lambda val: val == 'book'"],
    )

    @model_validator(mode="before")
    @staticmethod
    def validate_output_field_transformation(values):
        output_field, value, custom, switch = (
            values.get("output_field"),
            values.get("value"),
            values.get("custom"),
            values.get("switch"),
        )
        if (value or custom or switch) and not output_field:
            raise ValueError(
                "If 'transformation' is defined, 'output_field' also needs to be define.",
            )

        return values


class MainMappingModel(BasicModel):
    input_fields: list[str] = Field(
        ...,
        description="Input field for the switch.",
        examples=["cmi.object.type"],
    )
    output_fields: OutputMappingModel = Field(
        ...,
        description="Output field for the mapping.",
    )


class MetadataDateModel(BaseModel):
    publication: str = Field(
        ...,
        description="Publication date.",
        examples=["2023-01-01"],
    )
    update: str = Field(
        ...,
        description="Update date.",
        examples=["2023-02-01"],
    )


class MetadataModel(BasicModel):
    author: str = Field(
        ...,
        description="Author of the transformation config.",
        examples=["Your Name"],
    )
    date: MetadataDateModel = Field(
        ...,
        description="Dates related to the transformation config.",
    )


class MappingSchema(BaseModel):
    version: float = Field(
        ...,
        description="Version of the transformation config.",
        examples=[1.0],
    )
    input_format: str = Field(
        ...,
        description="Input format for the transformation.",
        examples=["SCORM"],
    )
    output_format: str = Field(
        ...,
        description="Output format for the transformation.",
        examples=["xAPI"],
    )
    mappings: list[MainMappingModel] = Field(
        ...,
        description="list of mappings.",
    )
    default_values: list[OutputMappingModel] = Field(
        default=[],
        description="list of default values.",
    )
    metadata: MetadataModel = Field(
        ...,
        description="Metadata for the transformation config.",
    )
