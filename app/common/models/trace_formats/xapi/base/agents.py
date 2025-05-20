"""Base xAPI `Agent` definitions."""

from abc import ABC
from typing import Literal

from pydantic import Field

from ..config import BaseModelWithConfig, NonEmptyStrictStr

from .common import IRI
from .ifi import (
    BaseXapiAccountIFI,
    BaseXapiMboxIFI,
    BaseXapiMboxSha1SumIFI,
    BaseXapiOpenIdIFI,
)


class BaseXapiAgentAccount(BaseModelWithConfig):
    """Pydantic model for `Agent` type `account` property."""

    homePage: IRI = Field(
        description="Home page of the account's service provider",
        examples=["http://www.example.com"],
    )
    name: NonEmptyStrictStr = Field(
        description="Unique id or name of the Actor's account", examples=["John Doe"]
    )


class BaseXapiAgentCommonProperties(BaseModelWithConfig, ABC):
    """Pydantic model for core `Agent` type property.

    It defines who performed the action.
    """

    objectType: Literal["Agent"] = "Agent"
    name: NonEmptyStrictStr | None = Field(
        None, description="full name of the Agent", examples=["John Doe"]
    )


class BaseXapiAgentWithMbox(BaseXapiAgentCommonProperties, BaseXapiMboxIFI):
    """Pydantic model for `Agent` type property.

    It is defined for agent type with a mailto IFI.
    """


class BaseXapiAgentWithMboxSha1Sum(
    BaseXapiAgentCommonProperties, BaseXapiMboxSha1SumIFI
):
    """Pydantic model for `Agent` type property.

    It is defined for agent type with a hash IFI.
    """


class BaseXapiAgentWithOpenId(BaseXapiAgentCommonProperties, BaseXapiOpenIdIFI):
    """Pydantic model for `Agent` type property.

    It is defined for agent type with an openID IFI.
    """


class BaseXapiAgentWithAccount(BaseXapiAgentCommonProperties, BaseXapiAccountIFI):
    """Pydantic model for `Agent` type property.

    It is defined for agent type with an account IFI.
    """


BaseXapiAgent = (
    BaseXapiAgentWithMbox
    | BaseXapiAgentWithMboxSha1Sum
    | BaseXapiAgentWithOpenId
    | BaseXapiAgentWithAccount
)
