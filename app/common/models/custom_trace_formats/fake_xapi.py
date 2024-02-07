from typing import Any, Optional

from pydantic import BaseModel, Field


class FakeXapiActorDefaultModel(BaseModel):
    type_str: Optional[str] = Field(default=None, alias="str")


class FakeXapiActorValueModel(BaseModel):
    type_int: Optional[int] = Field(default=None, alias="int")


class FakeXapiActorModel(BaseModel):
    type: Optional[Any] = Field(default=None)
    empty_val: str = Field(default=None)
    positive: int = Field(default=None)
    negative: str = Field(default=None)
    default: FakeXapiActorDefaultModel = Field(default=None)
    value: FakeXapiActorValueModel = Field(default=None)


class FakeXapiObjectModel(BaseModel):
    value: Optional[str] = Field(default=None)


class FakeXapiAuthorModel(BaseModel):
    description: Optional[str] = Field(default=None)


class FakeXapiContextModel(BaseModel):
    full_content: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class FakeXapiDefaultModel(BaseModel):
    type_dict: Optional[dict] = Field(default=None, alias="dict")
    type_list: Optional[list] = Field(default=None, alias="list")
    type_int: Optional[int] = Field(default=None, alias="int")
    type_float: Optional[float] = Field(default=None, alias="float")
    type_str: Optional[str] = Field(default=None, alias="str")
    type_boolean: Optional[bool] = Field(default=None, alias="boolean")
    empty: Optional[str] = Field(default=None)


class FakeXapiRootModel(BaseModel):
    actor: Optional[FakeXapiActorModel] = Field(default=None)
    object: Optional[FakeXapiObjectModel] = Field(default=None)
    author: Optional[FakeXapiAuthorModel] = Field(default=None)
    context: Optional[FakeXapiContextModel] = Field(default=None)
    default: Optional[FakeXapiDefaultModel] = Field(default=None)


class FakeXapiModel(BaseModel):
    xapi: Optional[FakeXapiRootModel] = Field(default=None)

    class Config:
        # Do not allow extra fields
        extra = "forbid"
