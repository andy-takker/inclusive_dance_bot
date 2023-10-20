import asyncio
import logging

from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from src.config import Settings
from src.db.factory import create_engine, create_session_factory
from src.db.tmp import update_url_cache
from src.db.uow.main import UnitOfWork
from src.dialogs import register_dialogs
from src.factory import create_bot, create_storage
from src.middlewares.cache import CacheMiddleware, CacheStorage
from src.middlewares.settings import SettingsMiddleware
from src.middlewares.uow import UowMiddleware
from src.ui_commands import set_ui_commands

logger = logging.getLogger(__name__)


async def main(settings: Settings) -> None:
    logging.basicConfig(level=logging.INFO)

    if settings.TELEGRAM_BOT_TOKEN.get_secret_value() == "default":
        raise ValueError("You should set env TELEGRAM_BOT_TOKEN")
    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(sessionmaker=session_factory)
    cache = CacheStorage()
    async with uow:
        await update_url_cache(uow=uow, cache=cache)

    bot = create_bot(settings=settings)
    storage = create_storage(settings=settings)
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(UowMiddleware(uow=uow))
    dp.update.outer_middleware(CacheMiddleware(cache=cache))
    register_dialogs(dp)
    setup_dialogs(dp)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        logger.info("Stopped")


if __name__ == "__main__":
    settings = Settings()
    asyncio.run(main(settings=settings))
