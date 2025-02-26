"""Base xAPI `Inverse Functional Identifier` definitions."""

from typing import Annotated

from pydantic import Field, StringConstraints

from ..config import NonEmptyStrictStr

from ..config import BaseModelWithConfig
from .common import IRI, URI, MailtoEmail


class BaseXapiAccount(BaseModelWithConfig):
    """Pydantic model for IFI `account` property."""

    homePage: IRI = Field(
        description="Home page of the account's service provider",
        examples=["http://www.example.com"],
    )
    name: NonEmptyStrictStr = Field(
        description="Unique id or name of the Actor's account", examples=["John Doe"]
    )


class BaseXapiMboxIFI(BaseModelWithConfig):
    """Pydantic model for mailto Inverse Functional Identifier."""

    mbox: MailtoEmail = Field(
        description="Agent's email address", examples=["mailto:test@example.com"]
    )


class BaseXapiMboxSha1SumIFI(BaseModelWithConfig):
    """Pydantic model for hash Inverse Functional Identifier."""

    mbox_sha1sum: Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{40}$")] = Field(
        description="SHA1 hash of the Agent's email address",
        examples=["ebd31e95054c018b10727ccffd2ef2ec3a016ee9"],
    )


class BaseXapiOpenIdIFI(BaseModelWithConfig):
    """Pydantic model for OpenID Inverse Functional Identifier."""

    openid: URI = Field(
        description="OpenID that uniquely identifies the Agent",
        examples=["http://johndoe.openid.example.org"],
    )


class BaseXapiAccountIFI(BaseModelWithConfig):
    """Pydantic model for account Inverse Functional Identifier."""

    account: BaseXapiAccount = Field(description="See BaseXapiAccount")
