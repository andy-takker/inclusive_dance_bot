import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.storage import Storage


@pytest_asyncio.fixture
async def uow(sessionmaker: async_sessionmaker[AsyncSession]) -> UnitOfWork:
    uow = UnitOfWork(sessionmaker=sessionmaker)
    async with uow:
        yield uow


@pytest_asyncio.fixture
async def storage(uow: UnitOfWork) -> Storage:
    return Storage(uow=uow)
