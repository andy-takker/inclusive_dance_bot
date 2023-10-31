from typing import NoReturn

from sqlalchemy import ScalarResult, insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import User
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import ANONYMOUS_USER, UserDto
from inclusive_dance_bot.exceptions import InclusiveDanceError, UserAlreadyExistsError


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def create(
        self, *, user_id: int, name: str, region: str, phone_number: str
    ) -> UserDto:
        stmt = (
            insert(User)
            .values(id=user_id, name=name, region=region, phone_number=phone_number)
            .returning(User)
        )
        try:
            result: ScalarResult[User] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return UserDto.from_orm(result.one())

    async def get_by_id(self, user_id: int) -> UserDto:
        obj = await self._get_by_id_or_none(obj_id=user_id)
        return UserDto.from_orm(obj) if obj else ANONYMOUS_USER

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__users":
            raise UserAlreadyExistsError from e
        raise InclusiveDanceError from e
