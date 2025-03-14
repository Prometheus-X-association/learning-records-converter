"""Base xAPI `Result` definitions."""

import re
from datetime import timedelta
from typing import Annotated, Any

from pydantic import BeforeValidator, Field, StrictBool, model_validator

from ..config import NonEmptyStrictStr

from ..config import BaseModelWithConfig
from .common import IRI


def ensure_duration_is_valid(value: Any) -> Any:
    """Check that duration is valid ISO 8601 format string."""
    if isinstance(value, timedelta):
        return value

    if not isinstance(value, str):
        raise ValueError("Duration must be expressed using ISO 8601 format string.")

    if "W" in value and not re.search(r"^P\d+W$", value):
        raise ValueError("Combining any other unit with weeks is not allowed.")

    return value


class BaseXapiResultScore(BaseModelWithConfig):
    """Pydantic model for result `score` property."""

    scaled: Annotated[float, Field(ge=-1, le=1, strict=True)] | None = Field(
        None,
        description="Normalized score related to the experience",
        examples=[0],
    )
    raw: Annotated[float, Field(strict=True)] | None = Field(
        None, description="Non-normalized score achieved by the Actor", examples=[10]
    )
    min: Annotated[float, Field(strict=True)] | None = Field(
        None, description="Lowest possible score", examples=[0]
    )
    max: Annotated[float, Field(strict=True)] | None = Field(
        None, description="Highest possible score", examples=[20]
    )

    @model_validator(mode="after")
    def check_raw_min_max_relation(self) -> Any:
        """Check the relationship `min < raw < max`."""
        if self.min:
            if self.max and self.min > self.max:
                raise ValueError("min cannot be greater than max")
            if self.raw and self.min > self.raw:
                raise ValueError("min cannot be greater than raw")
        if self.max:
            if self.raw and self.raw > self.max:
                raise ValueError("raw cannot be greater than max")
        return self


class BaseXapiResult(BaseModelWithConfig):
    """Pydantic model for `result` property."""

    score: BaseXapiResultScore | None = Field(
        None, description="See BaseXapiResultScore"
    )
    success: StrictBool | None = Field(
        None, description="Indicates whether the attempt on the Activity was successful"
    )
    completion: StrictBool | None = Field(
        None, description="Indicates whether the Activity was completed"
    )
    response: NonEmptyStrictStr | None = Field(
        None,
        description="Response for the given Activity",
        examples=["Wow, nice work!"],
    )
    duration: Annotated[timedelta, BeforeValidator(ensure_duration_is_valid)] | None = (
        Field(
            None,
            description="Duration over which the Statement occurred",
            examples=["PT1234S"],
        )
    )
    extensions: dict[IRI, str | int | bool | list | dict | None] | None = Field(
        None,
        description="Dictionary of other properties as needed",
        examples=[{"http://example.com/extensions/example-ext": 0}],
    )
