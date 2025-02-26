"""Base xAPI `Object` definitions (2)."""

# Nota bene: we split object definitions into `objects.py` and `unnested_objects.py`
# because of the circular dependency : objects -> context -> objects.

from datetime import datetime
from typing import Literal

from pydantic import Field

from ..config import BaseModelWithConfig
from .agents import BaseXapiAgent
from .attachments import BaseXapiAttachment
from .contexts import BaseXapiContext
from .groups import BaseXapiGroup
from .results import BaseXapiResult
from .unnested_objects import BaseXapiUnnestedObject
from .verbs import BaseXapiVerb


class BaseXapiSubStatement(BaseModelWithConfig):
    """Pydantic model for `SubStatement` type property."""

    actor: BaseXapiAgent | BaseXapiGroup = Field(
        description="See BaseXapiAgent and BaseXapiGroup"
    )
    verb: BaseXapiVerb = Field(description="See BaseXapiVerb")
    object: BaseXapiUnnestedObject = Field(description="See BaseXapiUnnestedObject")
    objectType: Literal["SubStatement"] = Field(description="Value `SubStatement`")
    result: BaseXapiResult | None = Field(
        None, description="Outcome related to the SubStatement"
    )
    context: BaseXapiContext | None = Field(
        None, description="Contextual information for the SubStatement"
    )
    timestamp: datetime | None = Field(
        None, description="Timestamp of when the event occurred"
    )
    attachments: list[BaseXapiAttachment] | None = Field(
        None, description="List of attachments"
    )


BaseXapiObject = BaseXapiUnnestedObject | BaseXapiSubStatement
