import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Feedback
from idb.db.uow import UnitOfWork
from idb.exceptions import InvalidUserIDError
from idb.generals.enums import FeedbackType
from idb.logic.feedback import create_feedback
from tests.factories import UserFactory


async def test_create_successful(uow: UnitOfWork, session: AsyncSession) -> None:
    user = await UserFactory.create_async()
    await create_feedback(
        uow=uow,
        user_id=user.id,
        type=FeedbackType.QUESTION,
        title="New question",
        text="Very important question",
    )
    query = select(Feedback).filter_by(user_id=user.id)
    feedback = (await session.scalars(query)).first()

    assert feedback.user_id == user.id
    assert feedback.type == FeedbackType.QUESTION
    assert feedback.title == "New question"
    assert feedback.text == "Very important question"


async def test_error_user_id(uow: UnitOfWork, session: AsyncSession) -> None:
    with pytest.raises(InvalidUserIDError):
        await create_feedback(
            uow=uow,
            user_id=1,
            type=FeedbackType.ADVERTISEMENT,
            title="Invalid user id",
            text="",
        )
