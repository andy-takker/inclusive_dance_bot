from typing import NoReturn

from sqlalchemy import ScalarResult, desc, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Entity
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import EntityDto
from inclusive_dance_bot.enums import EntityType
from inclusive_dance_bot.exceptions import EntityAlreadyExistsError, InclusiveDanceError


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
    ) -> EntityDto:
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
            return EntityDto.from_orm(result.one())

    async def get_entity_by_id(self, entity_id: int) -> EntityDto:
        obj = await self._get_by_id(entity_id)
        return EntityDto.from_orm(obj)

    async def get_all_entities(self) -> tuple[EntityDto, ...]:
        query = select(Entity).order_by(desc(Entity.weight), Entity.id)
        objs = (await self._session.scalars(query)).all()
        return tuple(EntityDto.from_orm(obj) for obj in objs)

    async def get_entities_by_type(self, entity_type: EntityType) -> list[EntityDto]:
        stmt = (
            select(Entity)
            .where(Entity.type == entity_type)
            .order_by(desc(Entity.weight), Entity.id)
        )

        objs = (await self._session.scalars(stmt)).all()
        return [EntityDto.from_orm(obj) for obj in objs]

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__entity":
            raise EntityAlreadyExistsError from e
        raise InclusiveDanceError from e
