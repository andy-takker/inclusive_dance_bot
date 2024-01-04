from datetime import datetime

from idb.db.uow import UnitOfWork
from idb.exceptions.base import InclusiveDanceError
from idb.generals.enums import FeedbackType


async def create_feedback(
    uow: UnitOfWork, user_id: int, type: FeedbackType, title: str, text: str
) -> None:
    """Создает новую обратную связь от пользователя"""
    try:
        await uow.feedbacks.create(
            user_id=user_id,
            type=type,
            title=title,
            text=text,
        )
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def set_feedback_as_viewed(
    uow: UnitOfWork,
    feedback_id: int,
    dt: datetime,
) -> None:
    try:
        await uow.feedbacks.update_by_id(
            feedback_id=feedback_id,
            is_viewed=True,
            viewed_at=dt,
        )
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def update_answered_feedback(
    uow: UnitOfWork,
    feedback_id: int,
    dt: datetime,
) -> None:
    try:
        await uow.feedbacks.update_by_id(
            feedback_id=feedback_id,
            is_answered=True,
            answered_at=dt,
        )
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
