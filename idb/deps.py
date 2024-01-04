import asyncio
from argparse import Namespace
from collections.abc import AsyncGenerator

from aiogram import Bot
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from idb.bot.factory import get_bot
from idb.db.uow import uow_context
from idb.db.utils import create_engine, create_session_factory
from idb.utils.cache import MemoryCache


def config_deps(arguments: Namespace) -> None:
    @dependency
    async def bot() -> Bot:
        return get_bot(
            telegram_bot_token=arguments.telegram_bot_token,
            parse_mode=arguments.telegram_parse_mode,
        )

    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_engine(
            connection_uri=arguments.pg_dsn,
            echo=arguments.debug,
        )
        yield engine
        await asyncio.shield(engine.dispose())

    @dependency
    async def sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_factory(engine=engine)

    @dependency
    async def cache(sessionmaker: async_sessionmaker[AsyncSession]) -> MemoryCache:
        cache = MemoryCache()
        async with uow_context(sessionmaker=sessionmaker) as uow:
            await cache.load_cache(uow=uow)

        return cache

    return
