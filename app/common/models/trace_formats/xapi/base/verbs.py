"""Base xAPI `Verb` definitions."""

from pydantic import Field

from ..config import BaseModelWithConfig
from .common import IRI, LanguageMap


class BaseXapiVerb(BaseModelWithConfig):
    """Pydantic model for `verb` property."""

    id: IRI = Field(
        description="Identifier for the verb",
        examples=["http://adlnet.gov/expapi/verbs/attended"],
    )
    display: LanguageMap | None = Field(
        None,
        description="Human-readable representation of the verb",
        examples=[{"en-GB": "attended", "en-US": "attended"}],
    )
