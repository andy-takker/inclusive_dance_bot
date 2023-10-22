import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import UserType
from inclusive_dance_bot.db.repositories.user_type import UserTypeRepository
from inclusive_dance_bot.dto import UserTypeDto
from inclusive_dance_bot.exceptions import UserTypeAlreadyExistsError
from tests.factories import UserTypeFactory

pytestmark = [pytest.mark.asyncio]


async def test_create_user_type(
    user_type_repo: UserTypeRepository, session: AsyncSession
) -> None:
    user_type = await user_type_repo.create(name="New user type")
    await session.commit()
    saved_user_type = await session.get(UserType, user_type.id)
    assert user_type == UserTypeDto.from_orm(saved_user_type)


async def test_invalid_double_create(user_type_repo: UserTypeRepository) -> None:
    await user_type_repo.create(name="New user type")
    with pytest.raises(UserTypeAlreadyExistsError):
        await user_type_repo.create(name="New user type")


async def test_get_all_user_types_empty(user_type_repo: UserTypeRepository) -> None:
    user_types = await user_type_repo.get_all_user_types()
    assert user_types == tuple()


async def test_get_all_user_types(user_type_repo: UserTypeRepository) -> None:
    user_types = await UserTypeFactory.create_batch_async(size=5)

    loaded_user_types = await user_type_repo.get_all_user_types()
    assert set(loaded_user_types) == {UserTypeDto.from_orm(ut) for ut in user_types}
