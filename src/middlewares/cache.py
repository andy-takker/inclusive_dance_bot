from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update


class CacheStorage:
    def __init__(self) -> None:
        self._storage: dict[str, Any] = {}

    def get(self, key: str, default: Any) -> Any | None:
        return self._storage.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def clear(self) -> None:
        self._storage.clear()

    def __getitem__(self, key: str) -> Any | None:
        return self._storage.get(key)


class CacheMiddleware(BaseMiddleware):
    def __init__(self, cache: CacheStorage) -> None:
        super().__init__()
        self.cache = cache

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        data["cache"] = self.cache
        return await handler(event, data)
