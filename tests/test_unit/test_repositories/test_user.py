import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import User as UserDb
from idb.db.repositories.user import UserRepository
from idb.exceptions import UserAlreadyExistsError
from idb.exceptions.user import UserNotFoundError
from idb.generals.models.user import User
from tests.factories import UserFactory


async def test_create_user(user_repo: UserRepository, session: AsyncSession) -> None:
    user = await user_repo.create(
        username="username",
        id=1,
        profile={
            "name": "user name",
            "region": "Tatuin",
            "phone_number": "+77777777777",
        },
        is_admin=False,
        is_superuser=False,
    )
    await session.commit()
    loaded_user = await session.get(UserDb, user.id)
    assert user == User.model_validate(loaded_user)


async def test_invalid_double_create(user_repo: UserRepository) -> None:
    await user_repo.create(
        username="username",
        id=1,
        is_admin=False,
        is_superuser=False,
        profile={
            "name": "user name",
            "region": "Tatuin",
            "phone_number": "+77777777777",
        },
    )
    with pytest.raises(UserAlreadyExistsError):
        await user_repo.create(
            username="username",
            id=1,
            is_admin=False,
            is_superuser=False,
            profile={
                "name": "user name",
                "region": "Tatuin",
                "phone_number": "+77777777777",
            },
        )


async def test_get_by_id(user_repo: UserRepository) -> None:
    user = await UserFactory.create_async()
    loaded_user = await user_repo.get_by_id(user.id)
    assert loaded_user == User.model_validate(user)


async def test_get_anonymous(user_repo: UserRepository) -> None:
    with pytest.raises(UserNotFoundError):
        await user_repo.get_by_id(-1)
