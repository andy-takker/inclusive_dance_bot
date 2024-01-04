from collections.abc import Mapping, Sequence
from typing import Any, NoReturn

from sqlalchemy import ScalarResult, func, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import (
    User as UserDb,
)
from idb.db.models import (
    UserType as UserTypeDb,
)
from idb.db.models import (
    UserTypeUser as UserTypeUserDb,
)
from idb.db.repositories.base import Repository
from idb.exceptions import (
    EntityNotFoundError,
    InclusiveDanceError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from idb.generals.models.user import User
from idb.generals.models.user_type import UserType


class UserRepository(Repository[UserDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=UserDb, session=session)

    async def create(
        self,
        *,
        id: int,
        username: str | None,
        is_admin: bool,
        is_superuser: bool,
        profile: Mapping[str, Any],
    ) -> User:
        stmt = (
            insert(UserDb)
            .values(
                id=id,
                username=username,
                is_admin=is_admin,
                is_superuser=is_superuser,
                profile=profile,
            )
            .returning(UserDb)
        )
        try:
            result: ScalarResult[UserDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return User.model_validate(result.one())

    async def update_by_id(self, user_id: int, **kwargs: Any) -> User:
        obj = await self._update(UserDb.id == user_id, **kwargs)
        return User.model_validate(obj)

    async def get_by_id(self, user_id: int) -> User:
        try:
            obj = await self._get_by_id(obj_id=user_id)
        except NoResultFound as e:
            raise UserNotFoundError from e
        return User.model_validate(obj)

    async def get_by_id_or_none(self, user_id: int) -> User | None:
        obj = await self._get_by_id_or_none(user_id)
        return User.model_validate(obj) if obj else None

    async def get_admin_list(self, include_superusers: bool) -> list[User]:
        stmt = select(UserDb).where(UserDb.is_admin.is_(True))
        if not include_superusers:
            stmt = stmt.where(UserDb.is_superuser.is_(False))
        return [User.model_validate(obj) for obj in await self._session.scalars(stmt)]

    async def add_to_admins(self, username: str) -> User:
        try:
            user = await self._update(
                UserDb.username == username,
                UserDb.is_admin.is_(False),
                is_admin=True,
            )
            return User.model_validate(user)
        except EntityNotFoundError as e:
            raise UserNotFoundError from e

    async def delete_from_admins(self, user_id: int) -> User:
        try:
            user = await self._update(
                UserDb.id == user_id,
                UserDb.is_admin.is_(True),
                is_admin=False,
            )
        except EntityNotFoundError as e:
            raise UserNotFoundError from e
        return User.model_validate(user)

    async def get_list_by_user_types(
        self, user_types: Sequence[UserType], ignore_admins: bool = True
    ) -> list[User]:
        stmt = select(UserDb)
        if len(user_types) != 0:
            stmt = (
                stmt.distinct(UserDb.id)
                .join(UserTypeUserDb, UserDb.id == UserTypeUserDb.user_id)
                .join(UserTypeDb, UserTypeUserDb.user_type_id == UserTypeDb.id)
                .where(UserTypeDb.name.in_([ut.name for ut in user_types]))
            )

        if ignore_admins:
            stmt = stmt.where(UserDb.is_admin.is_(False))
        result = await self._session.scalars(stmt)
        return [User.model_validate(obj) for obj in result]

    async def total_count(self) -> int:
        query = (
            select(func.count("*"))
            .select_from(UserDb)
            .where(UserDb.is_admin.is_(False))
        )
        return (await self._session.execute(query)).scalar_one()

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__users":
            raise UserAlreadyExistsError from e
        raise InclusiveDanceError from e
