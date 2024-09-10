from types import UnionType
from typing import Any, List, Union

from pydantic import BaseModel, field_validator
from pydantic.fields import FieldInfo
from pydantic_core import ValidationError
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import get_origin


class ExtendedTypeBaseModel(BaseModel):
    """Pydantic BaseModel with extended type for Fields.

    By using this BaseModel, all Fields with models as type will accept and auto detect
    all subclasses from models.

    Example
        class ModelA(BaseModel):
            name: str


        class ModelB(ModelA):
            name: str = Field(default="default")
            age: float


        class ModelC(ExtendedTypeBaseModel):
            object_a: ModelA


        ModelC(**{"object_a": {"age": 15}})  # OK > ModelB
        ModelC(**{"object_a": {"name": "bob"}})  # OK > ModelA
        ModelC(**{"object_a": {"name": "bob", "age": 15}})  # OK > ModelB
    """

    @classmethod
    def _get_subclasses(cls, annotation):
        """Get all child classes (subclasses) from a given model.

        Args:
            model (Type[BaseModel]): Model to get all child classes from.

        Returns:
            List[Type[BaseModel]]: All child classes with no depth restriction.
        """
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            yield annotation
            for subclass in annotation.__subclasses__():
                yield from cls._get_subclasses(subclass)
        elif hasattr(annotation, "__args__"):
            for arg in annotation.__args__:
                yield from cls._get_subclasses(arg)
        else:
            yield annotation

    @classmethod
    def _get_correct_value(cls, value: Any, annotations: List) -> Any:
        """Get the correct model instance depending on value

        Args:
            value (Any): Data for the model
            annotations (List): list of models

        Returns:
            Any: Either returns a model instance with the valid data or the exact passed value
        """
        for each_type in annotations:
            if issubclass(each_type, BaseModel) and isinstance(value, dict):
                try:
                    return each_type(**value)
                except ValidationError:
                    pass
        return value

    @field_validator("*", mode="before")
    @classmethod
    def validation(cls, value: Any, extra_info: ValidationInfo) -> Any:
        """Validator applied to all fields of a Model.
        The purpose is to auto detect child classes for a field that uses models for typing.

        Caution:
            This only applies to:
            - Direct pydantic model typing
            - Union or `|` typing
            - List typing

        Args:
            value (Any): Field value
            extra_info (ValidationInfo): Field extra information

        Returns:
            Any: Either returns a model instance with the valid data or the exact passed value
        """
        # Get FieldInfo
        field = cls.model_fields.get(
            extra_info.field_name if extra_info.field_name else "", None
        )

        # Check if condition gathered to treat
        if isinstance(field, FieldInfo) and (
            get_origin(field.annotation) in [list, Union, UnionType]
            or isinstance(field.annotation, BaseModel.__class__)
        ):
            # Get all child classes
            new_annotation = set()
            new_annotation.update(cls._get_subclasses(field.annotation))
            new_annotation = list(new_annotation)

            # Return correct instance
            if get_origin(field.annotation) is list and isinstance(value, list):
                return [
                    cls._get_correct_value(each_value, new_annotation)
                    for each_value in value
                ]

            return cls._get_correct_value(value, new_annotation)
        return value
