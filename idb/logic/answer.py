from idb.db.uow import UnitOfWork
from idb.exceptions.base import InclusiveDanceError
from idb.generals.models.answer import Answer


async def create_feedback_answer(
    uow: UnitOfWork,
    from_user_id: int,
    feedback_id: int,
    text: str,
) -> Answer:
    feedback = await uow.feedbacks.read_by_id(feedback_id)
    try:
        answer = await uow.answer.create(
            feedback_id=feedback_id,
            from_user_id=from_user_id,
            to_user_id=feedback.user_id,
            text=text,
        )
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    return answer
