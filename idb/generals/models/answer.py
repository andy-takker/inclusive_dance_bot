from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    feedback_id: int
    from_user_id: int
    to_user_id: int
    text: str
    created_at: datetime
    updated_at: datetime
