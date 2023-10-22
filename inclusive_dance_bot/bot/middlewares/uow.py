from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from inclusive_dance_bot.db.uow.main import UnitOfWork


class UowMiddleware(BaseMiddleware):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__()
        self.uow = uow

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        async with self.uow as uow:
            data["uow"] = uow
            return await handler(event, data)
