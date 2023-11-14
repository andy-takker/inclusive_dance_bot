from datetime import datetime, timedelta
from typing import Any, NoReturn

from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from inclusive_dance_bot.db.models import Mailing, MailingUserType
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import MailingDto
from inclusive_dance_bot.enums import MailingStatus
from inclusive_dance_bot.exceptions import (
    EntityNotFoundError,
    InclusiveDanceError,
    MailingNotFoundError,
)


class MailingRepository(Repository[Mailing]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Mailing, session=session)

    async def get_by_id(self, mailing_id: int) -> MailingDto:
        try:
            obj = await self._session.get_one(
                Mailing, mailing_id, options=(selectinload(Mailing.user_types),)
            )
            return MailingDto.from_orm(obj)
        except NoResultFound as e:
            raise MailingNotFoundError from e

    async def create(
        self,
        *,
        title: str,
        content: str,
        scheduled_at: datetime | None,
        status: MailingStatus,
        sent_at: datetime | None,
    ) -> MailingDto:
        stmt = (
            insert(Mailing)
            .values(
                title=title,
                content=content,
                scheduled_at=scheduled_at,
                status=status,
                sent_at=sent_at,
            )
            .returning(Mailing)
            .options(selectinload(Mailing.user_types))
        )
        try:
            result = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return MailingDto.from_orm(result.one())

    async def create_mailing_user_type(
        self, *, mailing_id: int, user_type_id: int
    ) -> MailingUserType:
        stmt = (
            insert(MailingUserType)
            .values(mailing_id=mailing_id, user_type_id=user_type_id)
            .returning(MailingUserType)
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
    ) -> list[MailingDto]:
        return await self.get_mailings(
            now, gap, Mailing.status == MailingStatus.SCHEDULED
        )

    async def get_archive_mailings(self) -> list[MailingDto]:
        return await self.get_mailings(
            None, None, Mailing.status != MailingStatus.SCHEDULED
        )

    async def get_mailings(
        self, now: datetime | None = None, gap: int | None = None, *args: Any
    ) -> list[MailingDto]:
        stmt = (
            select(Mailing)
            .options(selectinload(Mailing.user_types))
            .order_by(Mailing.created_at)
        )
        for arg in args:
            stmt = stmt.where(arg)
        if gap is not None and now is not None:
            stmt = stmt.where(Mailing.scheduled_at < now + timedelta(seconds=gap))

        result = await self._session.scalars(stmt)
        return [MailingDto.from_orm(obj) for obj in result]

    async def update_by_id(self, mailing_id: int, **kwargs: Any) -> MailingDto:
        obj = await self._update(Mailing.id == mailing_id, **kwargs)
        return MailingDto.from_orm(obj)

    async def _update(self, *args: Any, **kwargs: Any) -> Mailing:
        query = update(self._model).where(*args).values(**kwargs).returning(self._model)
        result = await self._session.scalars(
            select(self._model)
            .from_statement(query)
            .options(selectinload(Mailing.user_types))
        )
        try:
            obj = result.one()
            await self._session.flush(obj)
        except NoResultFound as e:
            raise EntityNotFoundError from e
        await self._session.refresh(obj)
        return obj

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        raise InclusiveDanceError from e
