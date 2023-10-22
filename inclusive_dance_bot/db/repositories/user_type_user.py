from typing import NoReturn

from sqlalchemy import ScalarResult, insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import UserTypeUser
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.exceptions import (
    InclusiveDanceError,
    InvalidUserIDError,
    InvalidUserTypeIDError,
    UserTypeUserAlreadyExistsError,
)


class UserTypeUserRepository(Repository[UserTypeUser]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=UserTypeUser, session=session)

    async def create(self, *, user_id: int, user_type_id: int) -> UserTypeUser:
        stmt = (
            insert(UserTypeUser)
            .values(
                user_id=user_id,
                user_type_id=user_type_id,
            )
            .returning(UserTypeUser)
        )
        try:
            result: ScalarResult[UserTypeUser] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return result.one()

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__user_type_user":
            raise UserTypeUserAlreadyExistsError from e
        if constraint == "fk__user_type_user__user_id__users":
            raise InvalidUserIDError from e
        if constraint == "fk__user_type_user__user_type_id__user_type":
            raise InvalidUserTypeIDError from e
        raise InclusiveDanceError from e
