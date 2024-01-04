from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt

from idb.generals.enums import MailingStatus
from idb.generals.models.user_type import UserType


class Mailing(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: PositiveInt
    scheduled_at: datetime | None
    sent_at: datetime | None
    cancelled_at: datetime | None
    status: MailingStatus
    title: str
    content: str
    user_types: Sequence[UserType]
