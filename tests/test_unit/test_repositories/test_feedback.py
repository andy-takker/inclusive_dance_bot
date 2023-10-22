import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Feedback
from inclusive_dance_bot.db.repositories.feedback import FeedbackRepository
from inclusive_dance_bot.dto import FeedbackDto
from inclusive_dance_bot.enums import FeedbackType
from inclusive_dance_bot.exceptions import InvalidUserIDError
from tests.factories import UserFactory

pytestmark = [pytest.mark.asyncio]


async def test_create(feedback_repo: FeedbackRepository, session: AsyncSession) -> None:
    user = await UserFactory.create_async()
    feedback = await feedback_repo.create(
        user_id=user.id,
        type=FeedbackType.QUESTION,
        title="Some question",
        text="Very important question",
    )
    loaded_feedback = await session.get(Feedback, feedback.id)
    assert feedback == FeedbackDto.from_orm(loaded_feedback)


async def test_invalid_user_id(feedback_repo: FeedbackRepository) -> None:
    with pytest.raises(InvalidUserIDError):
        await feedback_repo.create(
            user_id=-1,
            type=FeedbackType.ADVERTISEMENT,
            title="Some advertisement",
            text="With invalid user ID",
        )
