from typing import NoReturn

from sqlalchemy import ScalarResult, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import UserType as UserTypeDb
from idb.db.repositories.base import Repository
from idb.exceptions import (
    InclusiveDanceError,
    UserTypeAlreadyExistsError,
)
from idb.generals.models.user_type import UserType


class UserTypeRepository(Repository[UserTypeDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=UserTypeDb, session=session)

    async def create(self, *, name: str, id: int | None = None) -> UserType:
        data: dict[str, str | int] = dict(name=name)
        if id is not None:
            data["id"] = id
        stmt = insert(UserTypeDb).values(**data).returning(UserTypeDb)
        try:
            result: ScalarResult[UserTypeDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return UserType.model_validate(result.one())

    async def list(self) -> tuple[UserType, ...]:
        stmt = select(UserTypeDb).order_by(UserTypeDb.id)
        return tuple(
            UserType.model_validate(obj)
            for obj in (await self._session.scalars(stmt)).all()
        )

    async def upsert(self, *, id: int, name: str) -> UserType:
        stmt = (
            insert(UserTypeDb)
            .values(id=id, name=name)
            .on_conflict_do_update(
                index_elements=[UserTypeDb.id],
                set_={
                    "id": id,
                    "name": name,
                },
            )
            .returning(UserTypeDb)
        )
        try:
            result: ScalarResult[UserTypeDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return UserType.model_validate(result.one())

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint in ("pk__user_type", "ix__user_type__name"):
            raise UserTypeAlreadyExistsError from e
        raise InclusiveDanceError from e
