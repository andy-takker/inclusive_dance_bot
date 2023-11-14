from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import FeedbackType
from inclusive_dance_bot.exceptions.base import InclusiveDanceError


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
