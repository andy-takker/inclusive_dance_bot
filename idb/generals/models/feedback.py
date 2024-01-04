from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt

from idb.generals.enums import FeedbackType


class Feedback(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    user_id: int
    type: FeedbackType
    title: str
    text: str
    is_viewed: bool
    viewed_at: datetime | None
    is_answered: bool
    answered_at: datetime | None
    created_at: datetime
    updated_at: datetime
