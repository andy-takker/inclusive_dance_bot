import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import UserType as UserTypeDb
from idb.db.repositories.user_type import UserTypeRepository
from idb.exceptions import UserTypeAlreadyExistsError
from idb.generals.models.user_type import UserType
from tests.factories import UserTypeFactory


async def test_create_user_type(
    user_type_repo: UserTypeRepository, session: AsyncSession
) -> None:
    user_type = await user_type_repo.create(name="New user type")
    await session.commit()
    saved_user_type = await session.get(UserTypeDb, user_type.id)
    assert user_type == UserType.model_validate(saved_user_type)


async def test_invalid_double_create(user_type_repo: UserTypeRepository) -> None:
    await user_type_repo.create(name="New user type")
    with pytest.raises(UserTypeAlreadyExistsError):
        await user_type_repo.create(name="New user type")


async def test_get_list_empty(user_type_repo: UserTypeRepository) -> None:
    user_types = await user_type_repo.list()
    assert user_types == tuple()


async def test_get_list(user_type_repo: UserTypeRepository) -> None:
    user_types = await UserTypeFactory.create_batch_async(size=5)
    user_types.sort(key=lambda x: x.id)
    loaded_user_types = await user_type_repo.list()
    assert loaded_user_types == tuple(UserType.model_validate(ut) for ut in user_types)
