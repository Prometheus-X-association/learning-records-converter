"""Base xAPI `Context` definitions."""

from typing import Annotated, Any
from uuid import UUID

from pydantic import BeforeValidator, Field

from ..config import NonEmptyStrictStr

from ..config import BaseModelWithConfig
from .agents import BaseXapiAgent
from .common import IRI, LanguageTag
from .groups import BaseXapiGroup
from .unnested_objects import BaseXapiActivity, BaseXapiStatementRef


def ensure_list(value: Any) -> Any:
    """Transform single Activity Objects into list."""
    if not isinstance(value, list):
        return [value]
    else:
        return value


class BaseXapiContextContextActivities(BaseModelWithConfig):
    """Pydantic model for context `contextActivities` property."""

    parent: Annotated[list[BaseXapiActivity], BeforeValidator(ensure_list)] | None = (
        Field(
            None,
            description=(
                "An Activity with a direct relation to the statement's Activity"
            ),
        )
    )

    grouping: Annotated[list[BaseXapiActivity], BeforeValidator(ensure_list)] | None = (
        Field(
            None,
            description=(
                "An Activity with an indirect relation to the statement's Activity"
            ),
        )
    )
    category: Annotated[list[BaseXapiActivity], BeforeValidator(ensure_list)] | None = (
        Field(None, description="An Activity used to categorize the Statement")
    )
    other: Annotated[list[BaseXapiActivity], BeforeValidator(ensure_list)] | None = (
        Field(
            None,
            description=(
                "A contextActivity that doesn't fit one of the other properties"
            ),
        )
    )


class BaseXapiContext(BaseModelWithConfig):
    """Pydantic model for `context` property."""

    registration: UUID | None = Field(
        None, description="Registration that the Statement is associated with"
    )
    instructor: BaseXapiAgent | BaseXapiGroup | None = Field(
        None, description="Instructor that the Statement relates to"
    )
    team: BaseXapiGroup | None = Field(
        None, description="Team that this Statement relates to"
    )
    contextActivities: BaseXapiContextContextActivities | None = Field(
        None, description="See BaseXapiContextContextActivities"
    )
    revision: NonEmptyStrictStr | None = Field(
        None,
        description="Revision of the activity associated with this Statement",
        examples=["revision_of_the_learning_activity"],
    )
    platform: NonEmptyStrictStr | None = Field(
        None,
        description="Platform where the learning activity took place",
        examples=["platform_of_the_learning_activity"],
    )
    language: LanguageTag | None = Field(
        None,
        description="Language in which the experience occurred",
        examples=["en-US"],
    )
    statement: BaseXapiStatementRef | None = Field(
        None, description="Another Statement giving context for this Statement"
    )
    extensions: dict[IRI, str | int | bool | list | dict | None] | None = Field(
        None,
        description="Dictionary of other properties as needed",
        examples=[{"http://example.com/extensions/example-ext": 0}],
    )
