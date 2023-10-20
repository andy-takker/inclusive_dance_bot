from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, UserType, UserTypeUser
from src.db.repositories.base import Repository
from src.exceptions import InclusiveDanceError


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def get_by_id_or_none(self, user_id: int) -> User | None:
        return await self._get_by_id_or_none(obj_id=user_id)

    async def create(
        self, *, user_id: int, name: str, region: str, phone_number: str
    ) -> User:
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
            return result.one()

    async def create_user_type(self, name: str, id: int | None = None) -> UserType:
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
            return result.one()

    async def get_user_types(self) -> Sequence[UserType]:
        stmt = select(UserType).order_by(UserType.id)
        return (await self._session.scalars(stmt)).all()

    async def get_user_types_by_ids(self, ids: list[int]) -> Sequence[UserType]:
        stmt = select(UserType).where(UserType.id.in_(ids)).order_by(UserType.id)
        return (await self._session.scalars(stmt)).all()

    async def add_user_type_to_user(
        self, user_id: int, user_type_id: int
    ) -> UserTypeUser:
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

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise InclusiveDanceError from err
