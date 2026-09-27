from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Pagination(ApiModel):
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
    total: int = Field(ge=0)
