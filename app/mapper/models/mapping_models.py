from typing import Any

from pydantic import BaseModel


class FinalMappingModel(BaseModel):
    output_field: str | None
    value: Any
