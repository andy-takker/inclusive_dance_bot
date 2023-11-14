import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import UserTypeUser
from inclusive_dance_bot.db.repositories.user_type_user import UserTypeUserRepository
from inclusive_dance_bot.exceptions import (
    InvalidUserIDError,
    InvalidUserTypeIDError,
    UserTypeUserAlreadyExistsError,
)
from tests.factories import UserFactory, UserTypeFactory


async def test_create(
    user_type_user_repo: UserTypeUserRepository, session: AsyncSession
) -> None:
    user = await UserFactory.create_async()
    user_type = await UserTypeFactory.create_async()

    user_type_user = await user_type_user_repo.create(
        user_id=user.id,
        user_type_id=user_type.id,
    )
    await session.commit()
    utu = await session.get(
        UserTypeUser, ident={"user_type_id": user_type.id, "user_id": user.id}
    )
    assert utu == user_type_user


async def test_create_invalid_pk(
    user_type_user_repo: UserTypeUserRepository,
) -> None:
    user = await UserFactory.create_async()
    user_type = await UserTypeFactory.create_async()

    await user_type_user_repo.create(
        user_id=user.id,
        user_type_id=user_type.id,
    )
    with pytest.raises(UserTypeUserAlreadyExistsError):
        await user_type_user_repo.create(
            user_id=user.id,
            user_type_id=user_type.id,
        )


async def test_create_invalid_user_id(
    user_type_user_repo: UserTypeUserRepository,
) -> None:
    user_type = await UserTypeFactory.create_async()
    with pytest.raises(InvalidUserIDError):
        await user_type_user_repo.create(
            user_type_id=user_type.id,
            user_id=-1,
        )


async def test_create_invalid_user_type_id(
    user_type_user_repo: UserTypeUserRepository,
) -> None:
    user = await UserFactory.create_async()
    with pytest.raises(InvalidUserTypeIDError):
        await user_type_user_repo.create(
            user_type_id=-1,
            user_id=user.id,
        )
