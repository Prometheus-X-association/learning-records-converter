"""Base xAPI model configuration."""
from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints


class BaseModelWithConfig(BaseModel):
    """Pydantic model for base configuration shared among all models."""

    model_config = ConfigDict(
        extra="forbid", str_min_length=0, coerce_numbers_to_str=True
    )


class BaseExtensionModelWithConfig(BaseModel):
    """Pydantic model for extension configuration shared among all models."""

    model_config = ConfigDict(
        extra="allow", str_min_length=0, coerce_numbers_to_str=True
    )


NonEmptyStrictStr = Annotated[str, StringConstraints(min_length=1, strict=True)]
