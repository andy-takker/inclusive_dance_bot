from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs

from inclusive_dance_bot.bot.dialogs import register_dialogs
from inclusive_dance_bot.bot.middlewares.settings import SettingsMiddleware
from inclusive_dance_bot.bot.middlewares.storage import StorageMiddleware
from inclusive_dance_bot.bot.middlewares.uow import UowMiddleware
from inclusive_dance_bot.bot.middlewares.user import UserMiddleware
from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.factory import create_engine, create_session_factory
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.storage import Storage


def get_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
        parse_mode=ParseMode.HTML,
    )


@asynccontextmanager
async def get_dispatcher(settings: Settings) -> AsyncIterator[Dispatcher]:
    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(sessionmaker=session_factory)
    storage = Storage(uow=uow)

    async with uow:
        await storage.refresh_all()

    dp = Dispatcher(
        storage=get_storage(settings=settings),
        events_isolation=SimpleEventIsolation(),
    )
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(UowMiddleware(uow=uow))
    dp.update.outer_middleware(StorageMiddleware(storage=storage))
    dp.update.outer_middleware(UserMiddleware())
    register_dialogs(dp)
    setup_dialogs(dp)
    yield dp
    await engine.dispose()


def get_storage(settings: Settings) -> BaseStorage:
    if settings.DEBUG:
        return MemoryStorage()
    return RedisStorage.from_url(
        url=settings.build_redis_connection_uri(),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
