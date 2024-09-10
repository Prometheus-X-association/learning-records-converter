from typing import Any

from pydantic import BaseModel, Field


class FakeXapiActorDefaultModel(BaseModel):
    type_str: str | None = Field(default=None, alias="str")


class FakeXapiActorValueModel(BaseModel):
    type_int: int | None = Field(default=None, alias="int")


class FakeXapiActorModel(BaseModel):
    type: Any | None = Field(default=None)
    empty_val: str = Field(default=None)
    positive: int = Field(default=None)
    negative: str = Field(default=None)
    default: FakeXapiActorDefaultModel = Field(default=None)
    value: FakeXapiActorValueModel = Field(default=None)


class FakeXapiObjectModel(BaseModel):
    value: str | None = Field(default=None)


class FakeXapiAuthorModel(BaseModel):
    description: str | None = Field(default=None)


class FakeXapiContextModel(BaseModel):
    full_content: str | None = Field(default=None)
    description: str | None = Field(default=None)


class FakeXapiDefaultModel(BaseModel):
    type_dict: dict | None = Field(default=None, alias="dict")
    type_list: list | None = Field(default=None, alias="list")
    type_int: int | None = Field(default=None, alias="int")
    type_float: float | None = Field(default=None, alias="float")
    type_str: str | None = Field(default=None, alias="str")
    type_boolean: bool | None = Field(default=None, alias="boolean")
    empty: str | None = Field(default=None)


class FakeXapiRootModel(BaseModel):
    actor: FakeXapiActorModel | None = Field(default=None)
    object: FakeXapiObjectModel | None = Field(default=None)
    author: FakeXapiAuthorModel | None = Field(default=None)
    context: FakeXapiContextModel | None = Field(default=None)
    default: FakeXapiDefaultModel | None = Field(default=None)


class FakeXapiModel(BaseModel):
    fake_xapi: FakeXapiRootModel = Field(...)

    class Config:
        # Do not allow extra fields
        extra = "forbid"
