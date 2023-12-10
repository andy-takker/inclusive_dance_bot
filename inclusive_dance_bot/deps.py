from argparse import Namespace
from collections.abc import AsyncGenerator

from aiogram import Bot
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from inclusive_dance_bot.bot.factory import get_bot
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.db.utils import create_engine, create_session_factory


def config_deps(arguments: Namespace) -> None:
    @dependency
    async def bot() -> Bot:
        return get_bot(telegram_bot_token=arguments.telegram_bot_token)

    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_engine(
            connection_uri=arguments.pg_dsn,
            echo=arguments.debug,
        )
        yield engine
        await engine.dispose()

    @dependency
    async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_factory(engine=engine)

    @dependency
    async def uow(session_factory: async_sessionmaker[AsyncSession]) -> UnitOfWork:
        return UnitOfWork(sessionmaker=session_factory)

    return
