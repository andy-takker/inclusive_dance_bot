from collections.abc import Iterable

from aiogram.types import User as AiogramUser

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UserDto
from inclusive_dance_bot.exceptions.base import InclusiveDanceError


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


async def create_user(
    uow: UnitOfWork,
    user_id: int,
    username: str,
    name: str,
    region: str,
    phone_number: str,
    user_type_ids: Iterable[int],
) -> None:
    """Создает нового пользователя"""
    try:
        await uow.users.create(
            user_id=user_id,
            username=username,
            name=name,
            region=region,
            phone_number=phone_number,
        )
        for user_type_id in user_type_ids:
            await uow.user_type_users.create(user_id=user_id, user_type_id=user_type_id)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def add_user_to_admins(uow: UnitOfWork, username: str) -> None:
    try:
        await uow.users.add_to_admins(username=username)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def delete_from_admins(uow: UnitOfWork, user_id: int) -> None:
    try:
        await uow.users.delete_from_admins(user_id=user_id)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
