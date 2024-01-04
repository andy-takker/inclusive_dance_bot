from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from aiogram.types import User as TelegramUser
from pydantic import BaseModel, ConfigDict, NonNegativeInt

ANONYMOUS_USER_ID = 0


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: NonNegativeInt
    username: str | None
    is_admin: bool
    is_superuser: bool
    profile: Mapping[str, Any]

    @property
    def name(self) -> str | None:
        return self.profile.get("name")

    @property
    def region(self) -> str | None:
        return self.profile.get("region")

    @property
    def phone_number(self) -> str | None:
        return self.profile.get("phone_number")


@dataclass
class BotUser:
    telegram_user: TelegramUser
    user: User

    @property
    def is_superuser(self) -> bool:
        return self.user.is_superuser

    @property
    def is_admin(self) -> bool:
        return self.user.is_admin or self.is_superuser

    @property
    def is_anonymous(self) -> bool:
        return not bool(self.user.profile)
