from typing import NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import UserType
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import UserTypeDto
from inclusive_dance_bot.exceptions import (
    InclusiveDanceError,
    UserTypeAlreadyExistsError,
)


class UserTypeRepository(Repository[UserType]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=UserType, session=session)

    async def create(self, *, name: str, id: int | None = None) -> UserTypeDto:
        data: dict[str, str | int] = dict(name=name)
        if id is not None:
            data["id"] = id
        stmt = insert(UserType).values(**data).returning(UserType)
        try:
            result: ScalarResult[UserType] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return UserTypeDto.from_orm(result.one())

    async def get_all_user_types(self) -> tuple[UserTypeDto, ...]:
        stmt = select(UserType).order_by(UserType.id)
        return tuple(
            UserTypeDto.from_orm(obj)
            for obj in (await self._session.scalars(stmt)).all()
        )

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint in ("pk__user_type", "ix__user_type__name"):
            raise UserTypeAlreadyExistsError from e
        raise InclusiveDanceError from e
