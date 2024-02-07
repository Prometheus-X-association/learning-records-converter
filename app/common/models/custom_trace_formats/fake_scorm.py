from typing import Any, Optional

from pydantic import BaseModel, Field


class FakeScormActorModel(BaseModel):
    value: Optional[Any] = Field(default=None)


class FakeScormObjectModel(BaseModel):
    value: Optional[str] = Field(default=None)


class FakeScormAuthorModel(BaseModel):
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)


class FakeScormContextModel(BaseModel):
    where: Optional[str] = Field(default=None)
    why: Optional[str] = Field(default=None)


class FakeScormRootModel(BaseModel):
    actor: Optional[FakeScormActorModel] = Field(default=None)
    object: Optional[FakeScormObjectModel] = Field(default=None)
    author: Optional[FakeScormAuthorModel] = Field(default=None)
    context: Optional[FakeScormContextModel] = Field(default=None)


class FakeScormModel(BaseModel):
    scorm: Optional[FakeScormRootModel] = Field(default=None)

    class Config:
        # Do not allow extra fields
        extra = "forbid"
