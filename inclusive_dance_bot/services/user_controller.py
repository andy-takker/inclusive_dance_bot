from aiogram.types import User as AiogramUser

from inclusive_dance_bot.dto import UserDto


class MegaUser:
    def __init__(
        self, aiogram_user: AiogramUser, user: UserDto, superuser_ids: list[int]
    ) -> None:
        self._aiogram_user = aiogram_user
        self._user = user
        self._superuser_ids = superuser_ids

    def __repr__(self) -> str:
        return f"MegaUser(user={self._user},auser={self._aiogram_user})"

    @property
    def is_superuser(self) -> bool:
        return self._aiogram_user.id in self._superuser_ids

    @property
    def is_admin(self) -> bool:
        return self._user.is_admin or self.is_superuser

    @property
    def is_anonymous(self) -> bool:
        return self._user.id == 0
