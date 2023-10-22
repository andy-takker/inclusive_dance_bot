import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import User
from inclusive_dance_bot.db.repositories.user import UserRepository
from inclusive_dance_bot.dto import UserDto
from inclusive_dance_bot.exceptions import UserAlreadyExistsError
from tests.factories import UserFactory

pytestmark = [pytest.mark.asyncio]


async def test_create_user(user_repo: UserRepository, session: AsyncSession) -> None:
    user = await user_repo.create(
        user_id=1,
        name="user name",
        region="Tatuin",
        phone_number="+77777777",
    )
    await session.commit()
    loaded_user = await session.get(User, user.id)
    assert user == UserDto.from_orm(loaded_user)


async def test_invalid_double_create(user_repo: UserRepository) -> None:
    await user_repo.create(
        user_id=1,
        name="user name",
        region="Tatuin",
        phone_number="+77777777",
    )
    with pytest.raises(UserAlreadyExistsError):
        await user_repo.create(
            user_id=1,
            name="user name",
            region="Tatuin",
            phone_number="+77777777",
        )


async def test_get_by_id(user_repo: UserRepository) -> None:
    user = await UserFactory.create_async()
    loaded_user = await user_repo.get_by_id_or_none(user.id)
    assert loaded_user == UserDto.from_orm(user)


async def test_get_by_id_none(user_repo: UserRepository) -> None:
    empty = await user_repo.get_by_id_or_none(-1)
    assert empty is None
