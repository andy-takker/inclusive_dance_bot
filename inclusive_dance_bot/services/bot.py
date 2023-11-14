import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs
from aiomisc import Service

from inclusive_dance_bot.bot.dialogs import register_dialogs
from inclusive_dance_bot.bot.factory import get_storage
from inclusive_dance_bot.bot.middlewares.settings import SettingsMiddleware
from inclusive_dance_bot.bot.middlewares.storage import StorageMiddleware
from inclusive_dance_bot.bot.middlewares.uow import UowMiddleware
from inclusive_dance_bot.bot.middlewares.user import UserMiddleware
from inclusive_dance_bot.bot.ui_commands import set_ui_commands
from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage

log = logging.getLogger(__name__)


class AiogramBotService(Service):
    __dependencies__ = ("settings", "uow", "bot")

    settings: Settings
    uow: UnitOfWork
    bot: Bot

    async def start(self) -> None:
        if self.settings.TELEGRAM_BOT_TOKEN == "default":
            raise ValueError("You should set env TELEGRAM_BOT_TOKEN")

        log.info("Initialize bot")
        await set_ui_commands(self.bot)
        await self.bot.delete_webhook(drop_pending_updates=True)

        storage = Storage(uow=self.uow)

        async with self.uow:
            await storage.refresh_all()

        dp = Dispatcher(
            storage=get_storage(settings=self.settings),
            events_isolation=SimpleEventIsolation(),
        )
        dp.update.outer_middleware(SettingsMiddleware(settings=self.settings))
        dp.update.outer_middleware(UowMiddleware(uow=self.uow))
        dp.update.outer_middleware(StorageMiddleware(storage=storage))
        dp.update.outer_middleware(UserMiddleware())
        register_dialogs(dp)
        setup_dialogs(dp)

        self.start_event.set()
        log.info("Start polling")
        await dp.start_polling(self.bot)
