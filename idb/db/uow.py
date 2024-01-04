import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from idb.db.repositories.answer import AnswerRepository
from idb.db.repositories.feedback import FeedbackRepository
from idb.db.repositories.mailing import MailingRepository
from idb.db.repositories.submenu import SubmenuRepository
from idb.db.repositories.url import UrlRepository
from idb.db.repositories.user import UserRepository
from idb.db.repositories.user_type import UserTypeRepository
from idb.db.repositories.user_type_user import UserTypeUserRepository


class UnitOfWork:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._session = sessionmaker()
        self.submenus = SubmenuRepository(self._session)
        self.feedbacks = FeedbackRepository(self._session)
        self.mailings = MailingRepository(self._session)
        self.urls = UrlRepository(self._session)
        self.users = UserRepository(self._session)
        self.user_types = UserTypeRepository(self._session)
        self.user_type_users = UserTypeUserRepository(self._session)
        self.answer = AnswerRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
        task = asyncio.create_task(self._session.close())
        await asyncio.shield(task)


@asynccontextmanager
async def uow_context(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[UnitOfWork, None]:
    uow = UnitOfWork(sessionmaker=sessionmaker)
    yield uow
    await uow.rollback()
