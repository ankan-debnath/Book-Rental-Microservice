from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True  # for Pydantic v2
    }