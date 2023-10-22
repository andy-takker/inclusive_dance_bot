import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Entity
from inclusive_dance_bot.db.repositories.entity import EntityRepository
from inclusive_dance_bot.dto import EntityDto
from inclusive_dance_bot.enums import EntityType
from inclusive_dance_bot.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from tests.factories import EntityFactory

pytestmark = [pytest.mark.asyncio]


async def test_create_entity(
    entity_repo: EntityRepository, session: AsyncSession
) -> None:
    entity = await entity_repo.create(
        type=EntityType.INFORMATION,
        text="some entity",
        message="Very long message message",
    )
    await session.commit()
    saved_entity = await session.get(Entity, entity.id)
    assert entity == EntityDto.from_orm(saved_entity)


async def test_invalid_double_create(
    entity_repo: EntityRepository, session: AsyncSession
) -> None:
    await entity_repo.create(
        id=1,
        type=EntityType.INFORMATION,
        text="some entity",
        message="Very long message message",
    )
    await session.commit()
    with pytest.raises(EntityAlreadyExistsError):
        await entity_repo.create(
            id=1,
            type=EntityType.INFORMATION,
            text="some entity",
            message="Very long message message",
        )


async def test_get_entity_by_id(entity_repo: EntityRepository) -> None:
    entity = await EntityFactory.create_async()
    loaded_entity = await entity_repo.get_entity_by_id(entity.id)
    assert EntityDto.from_orm(entity) == loaded_entity


async def test_entity_not_found_by_id(entity_repo: EntityRepository) -> None:
    with pytest.raises(EntityNotFoundError):
        await entity_repo.get_entity_by_id(-1)


async def test_get_all_entities_emtpy(entity_repo: EntityRepository) -> None:
    empty = await entity_repo.get_all_entities()
    assert empty == tuple()


async def test_get_all_entities(entity_repo: EntityRepository) -> None:
    entities = await EntityFactory.create_batch_async(size=5)
    loaded_entities = await entity_repo.get_all_entities()
    assert {EntityDto.from_orm(e) for e in entities} == set(loaded_entities)


async def test_get_all_entities_order_by_weight(entity_repo: EntityRepository) -> None:
    third = await EntityFactory.create_async(weight=1)
    first = await EntityFactory.create_async(weight=100)
    second = await EntityFactory.create_async(weight=30)

    loaded_entities = await entity_repo.get_all_entities()
    assert loaded_entities == tuple(
        EntityDto.from_orm(e) for e in (first, second, third)
    )


async def test_get_entities_by_type(entity_repo: EntityRepository) -> None:
    target_type = await EntityFactory.create_async(type=EntityType.CHARITY)

    charity_entities = await entity_repo.get_entities_by_type(EntityType.CHARITY)

    assert set(charity_entities) == {EntityDto.from_orm(target_type)}


async def test_get_entities_by_type(entity_repo: EntityRepository) -> None:
    await EntityFactory.create_async(type=EntityType.EDUCATION)

    charity_entities = await entity_repo.get_entities_by_type(EntityType.CHARITY)
    assert set(charity_entities) == set()
