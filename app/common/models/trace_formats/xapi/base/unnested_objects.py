"""Base xAPI `Object` definitions (1)."""

from collections.abc import Sequence
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AnyUrl, Field, StringConstraints, field_validator

from ..config import NonEmptyStrictStr

from ..config import BaseModelWithConfig
from .agents import BaseXapiAgent
from .common import IRI, LanguageMap
from .groups import BaseXapiGroup


class BaseXapiActivityDefinition(BaseModelWithConfig):
    """Pydantic model for `Activity` type `definition` property."""

    name: LanguageMap | None = Field(
        None,
        description="Human-readable/visual name of the Activity",
        examples=[{"en-US": "Example course"}],
    )
    description: LanguageMap | None = Field(
        None,
        description="Description of the Activity",
        examples=[{"en-US": "A fictitious example course."}],
    )
    type: IRI | None = Field(
        None,
        description="Type of the Activity",
        examples=["http://www.example.co.uk/types/exampleactivitytype"],
    )
    moreInfo: AnyUrl | None = Field(
        None,
        description="URL to a document about the Activity",
        examples=["http://activitytype.example.com/345256"],
    )
    extensions: dict[IRI, str | int | bool | list | dict | None] | None = Field(
        None,
        description="Dictionary of other properties as needed",
        examples=[
            {
                "http://example.com/activitydefinitionextensions/room": {
                    "name": "Example Room",
                    "id": "http://example.com/rooms/342",
                }
            }
        ],
    )


class BaseXapiInteractionComponent(BaseModelWithConfig):
    """Pydantic model for an interaction component."""

    id: Annotated[str, StringConstraints(pattern=r"^[^\s]+$")] = Field(
        description="Identifier of the interaction component"
    )
    description: LanguageMap | None = Field(
        None, description="Description of the interaction"
    )


class BaseXapiActivityInteractionDefinition(BaseXapiActivityDefinition):
    """Pydantic model for `Activity` type `definition` property.

    It is defined for field with interaction properties.
    """

    interactionType: Literal[
        "true-false",
        "choice",
        "fill-in",
        "long-fill-in",
        "matching",
        "performance",
        "sequencing",
        "likert",
        "numeric",
        "other",
    ] = Field(description="Type of the interaction")
    correctResponsesPattern: list[NonEmptyStrictStr] | None = Field(
        None, description="Pattern for the correct response"
    )
    choices: list[BaseXapiInteractionComponent] | None = Field(
        None, description="List of selectable choices"
    )
    scale: list[BaseXapiInteractionComponent] | None = Field(
        None, description="List of options on the `likert` scale"
    )
    source: list[BaseXapiInteractionComponent] | None = Field(
        None, description="List of sources to be matched"
    )
    target: list[BaseXapiInteractionComponent] | None = Field(
        None, description="List of targets to be matched"
    )
    steps: list[BaseXapiInteractionComponent] | None = Field(
        None, description="List of the elements making up the interaction"
    )

    @field_validator("choices", "scale", "source", "target", "steps", mode="after")
    @classmethod
    def check_unique_ids(cls, value: Sequence[Any] | None) -> None:
        """Check the uniqueness of interaction components IDs."""
        if value and (len(value) != len({x.id for x in value if x})):
            raise ValueError("Duplicate InteractionComponents are not valid")


class BaseXapiActivity(BaseModelWithConfig):
    """Pydantic model for `Activity` type property."""

    id: IRI = Field(
        description="Identifier for a single unique Activity",
        examples=["http://example.adlnet.gov/xapi/example/activity"],
    )
    objectType: Literal["Activity"] | None = Field(None, description="Value `Activity`")
    definition: (
        BaseXapiActivityDefinition | BaseXapiActivityInteractionDefinition | None
    ) = Field(
        None,
        description=(
            "See BaseXapiActivityDefinition and BaseXapiActivityInteractionDefinition"
        ),
    )


class BaseXapiStatementRef(BaseModelWithConfig):
    """Pydantic model for `StatementRef` type property.

    Attributes:
        objectType (str): Consists of the .
        id (UUID): Consists of the .
    """

    id: UUID = Field(description="UUID of the referenced statement")
    objectType: Literal["StatementRef"] = Field(description="Value `StatementRef`")


BaseXapiUnnestedObject = (
    BaseXapiActivity | BaseXapiStatementRef | BaseXapiAgent | BaseXapiGroup
)
