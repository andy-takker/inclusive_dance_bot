from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.repositories.entity import EntityRepository
from src.db.repositories.url import UrlRepository
from src.db.repositories.user import UserRepository
from src.db.uow.base import UnitOfWorkBase


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def __aenter__(self) -> Self:
        self._session = self._sessionmaker()
        self.entities = EntityRepository(self._session)
        self.urls = UrlRepository(self._session)
        self.users = UserRepository(self._session)
        return await super().__aenter__()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
