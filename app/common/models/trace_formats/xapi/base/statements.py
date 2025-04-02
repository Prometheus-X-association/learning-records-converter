"""Base xAPI `Statement` definitions."""

import re
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Annotated, Any, Self
from uuid import UUID

from pydantic import BeforeValidator, Field, StringConstraints, model_validator

from ..config import BaseModelWithConfig
from .agents import BaseXapiAgent
from .attachments import BaseXapiAttachment
from .contexts import BaseXapiContext
from .groups import (
    BaseXapiAuthorityAnonymousGroup,
    BaseXapiGroup,
)
from .objects import BaseXapiObject
from .results import BaseXapiResult
from .unnested_objects import BaseXapiActivity
from .verbs import BaseXapiVerb

EMPTY_OBJECT_ALLOWED_FIELDS = ["definition", "extensions"]
VOIDED_VERB_ID = "http://adlnet.gov/expapi/verbs/voided"


def ensure_object_wo_objecttype_is_activity(value: Any) -> Any:
    """Check that if no objectType is provided, the object is an activity.

    See: https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Data.md#details-8
    """
    if isinstance(value, dict) and "objectType" not in value:
        return BaseXapiActivity.model_validate(value)

    return value


def ensure_timestamp_is_valid(value: Any) -> Any:
    """Check that timestamp doesn't end with '-0000' or '-00:00'."""
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        raise ValueError("timestamp must be expressed as string")

    if re.search("-00:?00$", value):
        raise ValueError("invalid timestamp offset")

    return value


class BaseXapiStatement(BaseModelWithConfig):
    """Pydantic model for base xAPI statements."""

    id: UUID | None = Field(
        None, description="Generated UUID string from the source event string"
    )
    actor: BaseXapiAgent | BaseXapiGroup = Field(
        description="Definition of who performed the action"
    )
    verb: BaseXapiVerb = Field(description="Action between an Actor and an Activity")
    object: Annotated[
        BaseXapiObject, BeforeValidator(ensure_object_wo_objecttype_is_activity)
    ] = Field(description="Definition of the thing that was acted on")
    result: BaseXapiResult | None = Field(
        None, description="Outcome related to the Statement"
    )
    context: BaseXapiContext | None = Field(
        None, description="Contextual information for the Statement"
    )
    timestamp: (
        Annotated[datetime, BeforeValidator(ensure_timestamp_is_valid)] | None
    ) = Field(None, description="Timestamp of when the event occurred")
    stored: Annotated[datetime, BeforeValidator(ensure_timestamp_is_valid)] | None = (
        Field(None, description="Timestamp of when the event was recorded")
    )
    authority: BaseXapiAgent | BaseXapiAuthorityAnonymousGroup | None = Field(
        None, description="Actor asserting this Statement is true"
    )
    version: Annotated[str, StringConstraints(pattern=r"^1\.0(?:\.[0-9]+)?$")] = Field(
        "1.0.0", description="Associated xAPI version of the Statement"
    )
    attachments: list[BaseXapiAttachment] | None = Field(
        None, description="List of attachments"
    )

    @model_validator(mode="before")
    @classmethod
    def check_absence_of_empty_and_invalid_values(cls, values: Any) -> Any:
        """Check the model for empty and invalid values.

        Check that the `context` field contains `platform` and `revision` fields
        only if the `object.objectType` property is equal to `Activity`.
        """
        if isinstance(values, Sequence):
            return values

        for field, value in values.items():
            if value is None:
                raise ValueError(f"{field}: invalid null value")

            if value == "":
                raise ValueError(f"{field}: invalid empty string")

            if field not in EMPTY_OBJECT_ALLOWED_FIELDS and value == {}:
                raise ValueError(f"{field}: invalid empty object")

            if isinstance(value, Mapping) and field != "extensions":
                cls.check_absence_of_empty_and_invalid_values(value)

        context = dict(values.get("context", {}))

        if context:
            platform = context.get("platform", {})
            revision = context.get("revision", {})
            object_type = dict(values["object"]).get("objectType", "Activity")

            if (platform or revision) and object_type != "Activity":
                raise ValueError(
                    "revision and platform properties can only be used if the "
                    "Statement's Object is an Activity"
                )

        return values

    @model_validator(mode="after")
    def check_voiding_requirements(self) -> Self:
        """Check if a voiding statement is valid."""
        if (
            str(self.verb.id) == VOIDED_VERB_ID
            and self.object.objectType != "StatementRef"
        ):
            raise ValueError("Statement verb voided does not use object 'StatementRef'")

        return self
