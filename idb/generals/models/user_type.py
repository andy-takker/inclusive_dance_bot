from pydantic import BaseModel, ConfigDict, PositiveInt


class UserType(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    name: str
