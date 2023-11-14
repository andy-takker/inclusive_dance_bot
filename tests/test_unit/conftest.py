import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage


@pytest.fixture
async def uow(sessionmaker: async_sessionmaker[AsyncSession]) -> UnitOfWork:
    uow = UnitOfWork(sessionmaker=sessionmaker)
    async with uow:
        yield uow


@pytest.fixture
async def storage(uow: UnitOfWork) -> Storage:
    return Storage(uow=uow)
