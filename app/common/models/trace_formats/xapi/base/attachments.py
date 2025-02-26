"""Base xAPI `Attachments` definitions."""

from typing import Annotated

from pydantic import AnyUrl, Field, StrictStr

from ..config import BaseModelWithConfig
from .common import IRI, LanguageMap


class BaseXapiAttachment(BaseModelWithConfig):
    """Pydantic model for `attachment` property."""

    usageType: IRI = Field(
        description="Identifies the usage of this Attachment",
        examples=["http://adlnet.gov/expapi/attachments/signature"],
    )
    display: LanguageMap = Field(
        description="Attachment's title", examples=[{"en-US": "Signature"}]
    )
    description: LanguageMap | None = Field(
        None,
        description="Attachment's description",
        examples=[{"en-US": "A test signature"}],
    )
    contentType: StrictStr = Field(
        description="Attachment's content type", examples=["application/octet-stream"]
    )
    length: Annotated[int, Field(strict=True)] = Field(
        description="Length of the Attachment's data in octets", examples=[4235]
    )
    sha2: StrictStr = Field(
        description="SHA-2 hash of the Attachment data",
        examples=["672fa5fa658017f1b72d65036f13379c6ab05d4ab3b6664908d8acf0b6a0c634"],
    )
    fileUrl: AnyUrl | None = Field(
        None,
        description="URL from which the Attachment can be retrieved",
        examples=["http://example.com/myfile"],
    )
