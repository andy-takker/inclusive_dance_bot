from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from inclusive_dance_bot.config import Settings


class SettingsMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        data["settings"] = self.settings
        return await handler(event, data)
