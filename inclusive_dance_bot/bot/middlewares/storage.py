from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from inclusive_dance_bot.logic.storage import Storage


class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage: Storage) -> None:
        super().__init__()
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        data["storage"] = self.storage
        return await handler(event, data)
