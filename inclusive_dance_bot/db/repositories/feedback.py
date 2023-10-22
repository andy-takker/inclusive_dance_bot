from typing import NoReturn

from sqlalchemy import ScalarResult, insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Feedback
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import FeedbackDto
from inclusive_dance_bot.enums import FeedbackType
from inclusive_dance_bot.exceptions import InclusiveDanceError, InvalidUserIDError


class FeedbackRepository(Repository[Feedback]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Feedback, session=session)

    async def create(
        self, *, user_id: int, type: FeedbackType, title: str, text: str
    ) -> FeedbackDto:
        query = (
            insert(Feedback)
            .values(
                user_id=user_id,
                type=type,
                title=title,
                text=text,
            )
            .returning(Feedback)
        )
        try:
            result: ScalarResult[Feedback] = await self._session.scalars(query)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return FeedbackDto.from_orm(result.one())

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "fk__feedback__user_id_users":
            raise InvalidUserIDError from e
        raise InclusiveDanceError from e
