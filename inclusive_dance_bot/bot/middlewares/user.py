from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiogram.types import User as AiogramUser

from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.user import MegaUser


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        aiogram_user: AiogramUser = data["event_from_user"]
        uow: UnitOfWork = data["uow"]
        settings: Settings = data["settings"]
        data["user"] = MegaUser(
            aiogram_user=aiogram_user,
            user=await uow.users.get_by_id(aiogram_user.id),
            superuser_ids=settings.TELEGRAM_BOT_ADMIN_IDS,
        )
        return await handler(event, data)
