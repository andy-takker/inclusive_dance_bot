import asyncio
import logging

from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from inclusive_dance_bot.bot.dialogs import register_dialogs
from inclusive_dance_bot.bot.factory import create_bot, create_storage
from inclusive_dance_bot.bot.middlewares.settings import SettingsMiddleware
from inclusive_dance_bot.bot.middlewares.storage import StorageMiddleware
from inclusive_dance_bot.bot.middlewares.uow import UowMiddleware
from inclusive_dance_bot.bot.ui_commands import set_ui_commands
from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.factory import create_engine, create_session_factory
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.storage import Storage

log = logging.getLogger(__name__)


async def start_bot(settings: Settings) -> None:
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format="%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S %d.%m.%Y",
    )
    log.info("Init bot")
    if settings.TELEGRAM_BOT_TOKEN.get_secret_value() == "default":
        raise ValueError("You should set env TELEGRAM_BOT_TOKEN")
    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(sessionmaker=session_factory)
    storage = Storage(uow=uow)
    async with uow:
        await storage.refresh_all()

    bot = create_bot(settings=settings)
    bot_storage = create_storage(settings=settings)
    dp = Dispatcher(storage=bot_storage)
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(UowMiddleware(uow=uow))
    dp.update.outer_middleware(StorageMiddleware(storage=storage))
    register_dialogs(dp)
    setup_dialogs(dp)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        log.info("Stopped")


def main() -> None:
    settings = Settings()
    asyncio.run(start_bot(settings=settings))


if __name__ == "__main__":
    main()
