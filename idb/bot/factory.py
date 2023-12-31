import ujson
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage


def get_bot(telegram_bot_token: str, parse_mode: ParseMode) -> Bot:
    return Bot(
        token=telegram_bot_token,
        parse_mode=parse_mode,
    )


def get_storage(debug: bool, redis_dsn: str) -> BaseStorage:
    if debug:
        return MemoryStorage()
    return RedisStorage.from_url(
        url=redis_dsn,
        key_builder=DefaultKeyBuilder(with_destiny=True),
        json_loads=ujson.loads,
        json_dumps=ujson.dumps,
    )
