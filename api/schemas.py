from pydantic import BaseModel, ConfigDict


class InputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)