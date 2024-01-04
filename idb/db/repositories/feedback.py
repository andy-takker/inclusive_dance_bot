from collections.abc import Sequence
from typing import Any, NoReturn

from sqlalchemy import desc, func, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Feedback as FeedbackDb
from idb.db.repositories.base import Repository
from idb.exceptions import InclusiveDanceError, InvalidUserIDError
from idb.generals.enums import FeedbackType
from idb.generals.models.feedback import Feedback


class FeedbackRepository(Repository[FeedbackDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=FeedbackDb, session=session)

    async def read_by_id(self, feedback_id: int) -> Feedback:
        obj = await self._get_by_id(feedback_id)
        return Feedback.model_validate(obj)

    async def create(
        self, *, user_id: int, type: FeedbackType, title: str, text: str
    ) -> Feedback:
        query = (
            insert(FeedbackDb)
            .values(
                user_id=user_id,
                type=type,
                title=title,
                text=text,
            )
            .returning(FeedbackDb)
        )
        try:
            obj = (await self._session.scalars(query)).one()
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return Feedback.model_validate(obj)

    async def total_count(self) -> int:
        return (
            await self._session.execute(select(func.count("*")).select_from(FeedbackDb))
        ).scalar_one()

    async def new_count(self) -> int:
        return (
            await self._session.execute(
                select(func.count("*"))
                .select_from(FeedbackDb)
                .where(FeedbackDb.is_viewed.is_(False))
            )
        ).scalar_one()

    async def new_items(self) -> Sequence[Feedback]:
        query = (
            select(FeedbackDb)
            .where(FeedbackDb.is_viewed.is_(False))
            .order_by(desc(FeedbackDb.created_at))
        )
        objs = (await self._session.scalars(query)).all()
        return [Feedback.model_validate(obj) for obj in objs]

    async def viewed_items(self) -> Sequence[Feedback]:
        query = (
            select(FeedbackDb)
            .where(FeedbackDb.is_viewed.is_(True))
            .order_by(desc(FeedbackDb.created_at))
        )
        objs = (await self._session.scalars(query)).all()
        return [Feedback.model_validate(obj) for obj in objs]

    async def archive_count(self) -> int:
        return (
            await self._session.execute(
                select(func.count("*"))
                .select_from(FeedbackDb)
                .where(FeedbackDb.is_viewed.is_(True))
            )
        ).scalar_one()

    async def update_by_id(self, feedback_id: int, **kwargs: Any) -> Feedback:
        obj = await self._update(FeedbackDb.id == feedback_id, **kwargs)
        return Feedback.model_validate(obj)

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "fk__feedback__user_id__users":
            raise InvalidUserIDError from e
        raise InclusiveDanceError from e
