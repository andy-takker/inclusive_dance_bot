from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from inclusive_dance_bot.config import Settings


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
        parse_mode=ParseMode.HTML,
    )


def create_storage(settings: Settings) -> BaseStorage:
    if settings.DEBUG:
        return MemoryStorage()
    return RedisStorage.from_url(
        url=settings.build_redis_connection_uri(),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
