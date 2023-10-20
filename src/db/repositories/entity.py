from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import ScalarResult, desc, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Entity
from src.db.repositories.base import Repository
from src.enums import EntityType
from src.exceptions import InclusiveDanceError


class EntityRepository(Repository[Entity]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Entity, session=session)

    async def create(
        self,
        type: EntityType,
        text: str,
        message: str,
        weight: int = 0,
        id: int | None = None,
    ) -> Entity:
        data = dict(type=type, text=text, message=message, weight=weight)
        if id is not None:
            data["id"] = id
        stmt = insert(Entity).values(**data).returning(Entity)
        try:
            result: ScalarResult[Entity] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return result.one()

    async def get_entity_by_id(self, entity_id: int) -> Entity:
        return await self._get_by_id(entity_id)

    async def get_entities_by_type(self, entity_type: EntityType) -> Sequence:
        stmt = (
            select(Entity)
            .where(Entity.type == entity_type)
            .order_by(desc(Entity.weight), Entity.id)
        )

        return (await self._session.scalars(stmt)).all()

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise InclusiveDanceError from err
