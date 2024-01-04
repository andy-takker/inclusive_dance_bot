from collections.abc import Sequence
from typing import Any, NoReturn

from sqlalchemy import ScalarResult, delete, desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Submenu as SubmenuDb
from idb.db.repositories.base import Repository
from idb.exceptions import (
    InclusiveDanceError,
    SubmenuAlreadyExistsError,
    SubmenuNotFoundError,
)
from idb.exceptions.base import EntityNotFoundError
from idb.generals.enums import SubmenuType
from idb.generals.models.submenu import Submenu


class SubmenuRepository(Repository[SubmenuDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=SubmenuDb, session=session)

    async def create(
        self,
        type: SubmenuType,
        button_text: str,
        message: str,
        weight: int = 0,
        id: int | None = None,
    ) -> Submenu:
        data = dict(type=type, button_text=button_text, message=message, weight=weight)
        if id is not None:
            data["id"] = id
        stmt = insert(SubmenuDb).values(**data).returning(SubmenuDb)
        try:
            result: ScalarResult[SubmenuDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)

        await self._session.flush()
        return Submenu.model_validate(result.one())

    async def upsert(
        self,
        *,
        id: int,
        type: SubmenuType,
        weight: int,
        button_text: str,
        message: str,
    ) -> Submenu:
        stmt = (
            insert(SubmenuDb)
            .values(
                id=id,
                type=type,
                weight=weight,
                button_text=button_text,
                message=message,
            )
            .on_conflict_do_update(
                index_elements=[SubmenuDb.id],
                set_={
                    "id": id,
                    "type": type,
                    "weight": weight,
                    "button_text": button_text,
                    "message": message,
                },
            )
            .returning(SubmenuDb)
        )
        try:
            result: ScalarResult[SubmenuDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return Submenu.model_validate(result.one())

    async def get_by_id(self, submenu_id: int) -> Submenu:
        try:
            obj = await self._get_by_id(submenu_id)
        except NoResultFound as e:
            raise SubmenuNotFoundError from e
        return Submenu.model_validate(obj)

    async def update_by_id(self, submenu_id: int, **kwargs: Any) -> Submenu:
        try:
            obj = await self._update(SubmenuDb.id == submenu_id, **kwargs)
        except EntityNotFoundError as e:
            raise SubmenuNotFoundError from e
        except IntegrityError as e:
            self._raise_error(e)
        return Submenu.model_validate(obj)

    async def delete_by_id(self, submenu_id: int) -> None:
        stmt = delete(SubmenuDb).where(SubmenuDb.id == submenu_id)
        await self._session.execute(stmt)

    async def list(self) -> tuple[Submenu, ...]:
        query = select(SubmenuDb).order_by(desc(SubmenuDb.weight), SubmenuDb.id)
        objs = (await self._session.scalars(query)).all()
        return tuple(Submenu.model_validate(obj) for obj in objs)

    async def get_list_by_type(self, submenu_type: SubmenuType) -> Sequence[Submenu]:
        stmt = (
            select(SubmenuDb)
            .where(SubmenuDb.type == submenu_type)
            .order_by(desc(SubmenuDb.weight), SubmenuDb.id)
        )

        objs = (await self._session.scalars(stmt)).all()
        return [Submenu.model_validate(obj) for obj in objs]

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__submenu":
            raise SubmenuAlreadyExistsError from e
        raise InclusiveDanceError from e
