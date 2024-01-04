from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from idb.utils.cache import AbstractBotCache


class CacheMiddleware(BaseMiddleware):
    def __init__(self, cache: AbstractBotCache) -> None:
        super().__init__()
        self._cache = cache

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        data["cache"] = self._cache
        return await handler(event, data)
