from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Answer as AnswerDb
from idb.db.repositories.base import Repository
from idb.exceptions.base import InclusiveDanceError
from idb.exceptions.user import InvalidUserIDError
from idb.generals.models.answer import Answer


class AnswerRepository(Repository[AnswerDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=AnswerDb, session=session)

    async def create(
        self,
        *,
        feedback_id: int,
        from_user_id: int,
        to_user_id: int,
        text: str,
    ) -> Answer:
        query = (
            insert(AnswerDb)
            .values(
                feedback_id=feedback_id,
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                text=text,
            )
            .returning(AnswerDb)
        )
        try:
            obj = (await self._session.scalars(query)).one()
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return Answer.model_validate(obj)

    async def history(self, feedback_id: int) -> Sequence[Answer]:
        query = (
            select(AnswerDb)
            .where(AnswerDb.feedback_id == feedback_id)
            .order_by(AnswerDb.created_at)
        )
        objs = (await self._session.scalars(query)).all()
        return [Answer.model_validate(obj) for obj in objs]

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "fk__answer__to_user_id__users":
            raise InvalidUserIDError from e
        if constraint == "fk__answer__from_user_id__users":
            raise InvalidUserIDError from e
        raise InclusiveDanceError from e
