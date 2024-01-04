import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Feedback as FeedbackDb
from idb.db.repositories.feedback import FeedbackRepository
from idb.exceptions import InvalidUserIDError
from idb.generals.enums import FeedbackType
from idb.generals.models.feedback import Feedback
from tests.factories import UserFactory


async def test_create(feedback_repo: FeedbackRepository, session: AsyncSession) -> None:
    user = await UserFactory.create_async()
    feedback = await feedback_repo.create(
        user_id=user.id,
        type=FeedbackType.QUESTION,
        title="Some question",
        text="Very important question",
    )
    loaded_feedback = await session.get(FeedbackDb, feedback.id)
    assert feedback == Feedback.model_validate(loaded_feedback)


async def test_invalid_user_id(feedback_repo: FeedbackRepository) -> None:
    with pytest.raises(InvalidUserIDError):
        await feedback_repo.create(
            user_id=-1,
            type=FeedbackType.ADVERTISEMENT,
            title="Some advertisement",
            text="With invalid user ID",
        )
