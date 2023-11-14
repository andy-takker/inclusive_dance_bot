import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import User, UserTypeUser
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.exceptions import (
    InvalidUserTypeIDError,
    UserAlreadyExistsError,
)
from inclusive_dance_bot.logic.user import create_user
from tests.factories import UserFactory, UserTypeFactory


async def test_create_successful(uow: UnitOfWork, session: AsyncSession) -> None:
    user_types = await UserTypeFactory.create_batch_async(size=3)
    user_id = 1
    await create_user(
        uow=uow,
        username="username",
        user_id=user_id,
        name="New user",
        region="Some region",
        phone_number="+79999999",
        user_type_ids=tuple(ut.id for ut in user_types),
    )

    user = await session.get(User, user_id)
    assert user is not None

    user_type_users = (
        await session.scalars(
            select(UserTypeUser).where(UserTypeUser.user_id == user_id)
        )
    ).all()
    assert {(utu.user_id, utu.user_type_id) for utu in user_type_users} == {
        (user_id, ut.id) for ut in user_types
    }


async def test_error_user_type(uow: UnitOfWork, session: AsyncSession) -> None:
    user_id = 1
    with pytest.raises(InvalidUserTypeIDError):
        await create_user(
            uow=uow,
            user_id=user_id,
            username="username",
            name="New user",
            region="Some region",
            phone_number="+79999999",
            user_type_ids=(-1,),
        )
    user = await session.get(User, user_id)
    assert user is None


async def test_error_user_id_already_exists(uow: UnitOfWork) -> None:
    user = await UserFactory.create_async()
    with pytest.raises(UserAlreadyExistsError):
        await create_user(
            uow=uow,
            user_id=user.id,
            username="username",
            name="New user",
            region="Some region",
            phone_number="+79999999",
            user_type_ids=[],
        )
