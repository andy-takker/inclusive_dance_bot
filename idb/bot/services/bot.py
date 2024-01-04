import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiogram_dialog.widgets.text.jinja import setup_jinja
from aiomisc import Service
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from idb.bot.dialogs.router import register_dialogs
from idb.bot.factory import get_storage
from idb.bot.handlers import on_unknown_intent, on_unknown_state
from idb.bot.middlewares.cache import CacheMiddleware
from idb.bot.middlewares.uow import UowMiddleware
from idb.bot.middlewares.user import UserMiddleware
from idb.bot.ui_commands import set_ui_commands
from idb.bot.utils import as_local_fmt
from idb.utils.cache import AbstractBotCache

log = logging.getLogger(__name__)


class AiogramBotService(Service):
    __required__ = ("debug", "redis_dsn", "telegram_bot_admin_ids")

    __dependencies__ = ("sessionmaker", "bot", "cache")

    debug: bool
    redis_dsn: str
    telegram_bot_admin_ids: list[int]

    sessionmaker: async_sessionmaker[AsyncSession]
    bot: Bot
    cache: AbstractBotCache

    async def start(self) -> None:
        log.info("Initialize bot")
        await set_ui_commands(self.bot)
        await self.bot.delete_webhook(drop_pending_updates=True)

        dp = Dispatcher(
            storage=get_storage(
                debug=self.debug,
                redis_dsn=self.redis_dsn,
            ),
            events_isolation=SimpleEventIsolation(),
        )
        dp.update.outer_middleware(UowMiddleware(sessionmaker=self.sessionmaker))
        dp.update.outer_middleware(CacheMiddleware(cache=self.cache))
        dp.update.outer_middleware(
            UserMiddleware(telegram_bot_admin_ids=self.telegram_bot_admin_ids)
        )
        register_dialogs(dp)
        setup_dialogs(dp)
        dp.errors.register(
            on_unknown_intent,
            ExceptionTypeFilter(UnknownIntent),
        )
        dp.errors.register(
            on_unknown_state,
            ExceptionTypeFilter(UnknownState),
        )
        setup_jinja(
            dp=self.bot,
            filters={
                "as_local_fmt": as_local_fmt,
            },
        )
        self.start_event.set()
        log.info("Start polling")
        await dp.start_polling(self.bot)
