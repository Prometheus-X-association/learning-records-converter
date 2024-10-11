from typing import Any

from pydantic import BaseModel, Field


class FakeScormActorModel(BaseModel):
    value: Any | None = Field(default=None)


class FakeScormObjectModel(BaseModel):
    value: str | None = Field(default=None)


class FakeScormAuthorModel(BaseModel):
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    age: int | None = Field(default=None)


class FakeScormContextModel(BaseModel):
    where: str | None = Field(default=None)
    why: str | None = Field(default=None)


class FakeScormRootModel(BaseModel):
    actor: FakeScormActorModel | None = Field(default=None)
    object: FakeScormObjectModel | None = Field(default=None)
    author: FakeScormAuthorModel | None = Field(default=None)
    context: FakeScormContextModel | None = Field(default=None)


class FakeScormModel(BaseModel):
    fake_scorm: FakeScormRootModel = Field(...)

    class Config:
        # Do not allow extra fields
        extra = "forbid"
