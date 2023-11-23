from collections.abc import AsyncGenerator

from aiogram import Bot
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from inclusive_dance_bot.bot.factory import get_bot
from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.db.utils import create_engine, create_session_factory


def config_deps(app_settings: Settings) -> None:
    @dependency
    async def settings() -> Settings:
        return app_settings

    @dependency
    async def bot(settings: Settings) -> Bot:
        return get_bot(settings=settings)

    @dependency
    async def engine(settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_engine(
            connection_uri=settings.build_db_connection_uri(),
            echo=settings.DEBUG,
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
