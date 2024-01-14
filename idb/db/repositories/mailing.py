from datetime import datetime, timedelta
from typing import Any, NoReturn

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from idb.db.models import Mailing as MailingDb
from idb.db.models import MailingUserType as MailingUserTypeDb
from idb.db.repositories.base import Repository
from idb.exceptions import (
    InclusiveDanceError,
    MailingNotFoundError,
)
from idb.generals.enums import MailingStatus
from idb.generals.models.mailing import Mailing


class MailingRepository(Repository[MailingDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=MailingDb, session=session)

    async def get_by_id(self, mailing_id: int) -> Mailing:
        try:
            obj = await self._session.get_one(
                MailingDb, mailing_id, options=(selectinload(MailingDb.user_types),)
            )
            return Mailing.model_validate(obj)
        except NoResultFound as e:
            raise MailingNotFoundError from e

    async def create(
        self,
        *,
        author_id: int,
        title: str,
        content: str,
        scheduled_at: datetime | None,
        status: MailingStatus,
        sent_at: datetime | None,
    ) -> Mailing:
        stmt = (
            insert(MailingDb)
            .values(
                author_id=author_id,
                title=title,
                content=content,
                scheduled_at=scheduled_at,
                status=status,
                sent_at=sent_at,
            )
            .returning(MailingDb)
            .options(selectinload(MailingDb.user_types))
        )
        try:
            obj = (await self._session.scalars(stmt)).one()
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return Mailing.model_validate(obj)

    async def create_mailing_user_type(
        self, *, mailing_id: int, user_type_id: int
    ) -> MailingUserTypeDb:
        stmt = (
            insert(MailingUserTypeDb)
            .values(mailing_id=mailing_id, user_type_id=user_type_id)
            .returning(MailingUserTypeDb)
        )
        try:
            result = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return result.one()

    async def get_new_mailings(
        self, now: datetime | None = None, gap: int | None = None
    ) -> list[Mailing]:
        return await self.get_mailings(
            now, gap, MailingDb.status == MailingStatus.SCHEDULED
        )

    async def get_archive_mailings(self) -> list[Mailing]:
        return await self.get_mailings(
            None, None, MailingDb.status != MailingStatus.SCHEDULED
        )

    async def get_mailings(
        self, now: datetime | None = None, gap: int | None = None, *args: Any
    ) -> list[Mailing]:
        stmt = (
            select(MailingDb)
            .options(selectinload(MailingDb.user_types))
            .order_by(MailingDb.created_at)
        )
        for arg in args:
            stmt = stmt.where(arg)
        if gap is not None and now is not None:
            stmt = stmt.where(MailingDb.scheduled_at < now + timedelta(seconds=gap))

        result = await self._session.scalars(stmt)
        return [Mailing.model_validate(obj) for obj in result]

    async def update_by_id(self, mailing_id: int, **kwargs: Any) -> Mailing:
        obj = await self._update(MailingDb.id == mailing_id, **kwargs)
        return Mailing.model_validate(obj)

    async def _update(self, *args: Any, **kwargs: Any) -> MailingDb:
        query = update(self._model).where(*args).values(**kwargs).returning(self._model)
        result = await self._session.scalars(
            select(self._model)
            .from_statement(query)
            .options(selectinload(MailingDb.user_types))
        )
        try:
            obj = result.one()
            await self._session.flush(obj)
        except NoResultFound as e:
            raise MailingNotFoundError from e
        await self._session.refresh(obj)
        return obj

    async def total_count(self) -> int:
        return (
            await self._session.execute(select(func.count("*")).select_from(MailingDb))
        ).scalar_one()

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        raise InclusiveDanceError from e
