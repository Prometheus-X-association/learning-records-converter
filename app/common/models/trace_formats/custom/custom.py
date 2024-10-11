from pydantic import BaseModel, ConfigDict


class CustomDataModel(BaseModel):
    model_config = ConfigDict(extra="allow")
