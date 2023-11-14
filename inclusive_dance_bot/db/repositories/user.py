from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import User, UserType, UserTypeUser
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import ANONYMOUS_USER, UserDto, UserTypeDto
from inclusive_dance_bot.exceptions import (
    EntityNotFoundError,
    InclusiveDanceError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def create(
        self, *, user_id: int, username: str, name: str, region: str, phone_number: str
    ) -> UserDto:
        stmt = (
            insert(User)
            .values(
                id=user_id,
                username=username,
                name=name,
                region=region,
                phone_number=phone_number,
            )
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

    async def get_admin_list(self) -> list[UserDto]:
        stmt = select(User).where(User.is_admin.is_(True))
        return [UserDto.from_orm(obj) for obj in await self._session.scalars(stmt)]

    async def add_to_admins(self, username: str) -> UserDto:
        try:
            user = await self._update(
                User.username == username, User.is_admin.is_(False), is_admin=True
            )
            return UserDto.from_orm(user)
        except EntityNotFoundError as e:
            raise UserNotFoundError from e

    async def delete_from_admins(self, user_id: int) -> UserDto:
        try:
            user = await self._update(
                User.id == user_id, User.is_admin.is_(True), is_admin=False
            )
            return UserDto.from_orm(user)
        except EntityNotFoundError as e:
            raise UserNotFoundError from e

    async def get_list_by_user_types(
        self, user_types: Sequence[UserTypeDto], ignore_admins: bool = True
    ) -> list[UserDto]:
        stmt = select(User)
        if len(user_types) != 0:
            stmt = (
                stmt.distinct(User.id)
                .join(UserTypeUser, User.id == UserTypeUser.user_id)
                .join(UserType, UserTypeUser.user_type_id == UserType.id)
                .where(UserType.name.in_([ut.name for ut in user_types]))
            )

        if ignore_admins:
            stmt = stmt.where(User.is_admin.is_(False))
        result = await self._session.scalars(stmt)
        return [UserDto.from_orm(obj) for obj in result]

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__users":
            raise UserAlreadyExistsError from e
        raise InclusiveDanceError from e
