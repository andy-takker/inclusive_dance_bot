from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from inclusive_dance_bot.db.repositories.feedback import FeedbackRepository
from inclusive_dance_bot.db.repositories.submenu import SubmenuRepository
from inclusive_dance_bot.db.repositories.url import UrlRepository
from inclusive_dance_bot.db.repositories.user import UserRepository
from inclusive_dance_bot.db.repositories.user_type import UserTypeRepository
from inclusive_dance_bot.db.repositories.user_type_user import UserTypeUserRepository
from inclusive_dance_bot.db.uow.base import UnitOfWorkBase


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def __aenter__(self) -> Self:
        self._session = self._sessionmaker()
        self.submenus = SubmenuRepository(self._session)
        self.feedbacks = FeedbackRepository(self._session)
        self.urls = UrlRepository(self._session)
        self.users = UserRepository(self._session)
        self.user_types = UserTypeRepository(self._session)
        self.user_type_users = UserTypeUserRepository(self._session)
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        await self._session.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
