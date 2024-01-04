from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiogram.types import User as TelegramUser

from idb.db.uow import UnitOfWork
from idb.generals.models.user import BotUser, User


class UserMiddleware(BaseMiddleware):
    _telegram_bot_admin_ids: list[int]

    def __init__(self, telegram_bot_admin_ids: list[int]) -> None:
        self._telegram_bot_admin_ids = telegram_bot_admin_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        telegram_user: TelegramUser = data["event_from_user"]
        uow: UnitOfWork = data["uow"]
        user = await self._get_or_create_user(uow=uow, telegram_user=telegram_user)
        data["user"] = BotUser(
            telegram_user=telegram_user,
            user=user,
        )
        return await handler(event, data)

    async def _get_or_create_user(
        self,
        uow: UnitOfWork,
        telegram_user: TelegramUser,
    ) -> User:
        user = await uow.users.get_by_id_or_none(telegram_user.id)
        if user is None:
            is_superuser = telegram_user.id in self._telegram_bot_admin_ids
            user = await uow.users.create(
                id=telegram_user.id,
                username=telegram_user.username,
                is_admin=is_superuser,
                is_superuser=is_superuser,
                profile=dict(),
            )
            await uow.commit()
        return user
