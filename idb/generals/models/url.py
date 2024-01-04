from pydantic import BaseModel, ConfigDict, PositiveInt


class Url(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    slug: str
    value: str

    def __str__(self) -> str:
        return self.value
