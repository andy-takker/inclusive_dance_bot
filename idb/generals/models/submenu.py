from pydantic import BaseModel, ConfigDict, PositiveInt

from idb.generals.enums import SubmenuType


class Submenu(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    type: SubmenuType
    weight: int
    button_text: str
    message: str
