from typing import NoReturn

from sqlalchemy import ScalarResult, desc, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Submenu
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import SubmenuDto
from inclusive_dance_bot.enums import SubmenuType
from inclusive_dance_bot.exceptions import (
    InclusiveDanceError,
    SubmenuAlreadyExistsError,
    SubmenuNotFoundError,
)


class SubmenuRepository(Repository[Submenu]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Submenu, session=session)

    async def create(
        self,
        type: SubmenuType,
        text: str,
        message: str,
        weight: int = 0,
        id: int | None = None,
    ) -> SubmenuDto:
        data = dict(type=type, text=text, message=message, weight=weight)
        if id is not None:
            data["id"] = id
        stmt = insert(Submenu).values(**data).returning(Submenu)
        try:
            result: ScalarResult[Submenu] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return SubmenuDto.from_orm(result.one())

    async def get_by_id(self, submenu_id: int) -> SubmenuDto:
        try:
            obj = await self._get_by_id(submenu_id)
            return SubmenuDto.from_orm(obj)
        except NoResultFound as e:
            raise SubmenuNotFoundError from e

    async def get_list(self) -> tuple[SubmenuDto, ...]:
        query = select(Submenu).order_by(desc(Submenu.weight), Submenu.id)
        objs = (await self._session.scalars(query)).all()
        return tuple(SubmenuDto.from_orm(obj) for obj in objs)

    async def get_list_by_type(self, submenu_type: SubmenuType) -> list[SubmenuDto]:
        stmt = (
            select(Submenu)
            .where(Submenu.type == submenu_type)
            .order_by(desc(Submenu.weight), Submenu.id)
        )

        objs = (await self._session.scalars(stmt)).all()
        return [SubmenuDto.from_orm(obj) for obj in objs]

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__submenu":
            raise SubmenuAlreadyExistsError from e
        raise InclusiveDanceError from e
