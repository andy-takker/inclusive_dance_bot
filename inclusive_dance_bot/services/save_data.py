from collections.abc import Iterable

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.enums import FeedbackType
from inclusive_dance_bot.exceptions import InclusiveDanceError
from inclusive_dance_bot.services.storage import Storage


async def save_new_user(
    uow: UnitOfWork,
    user_id: int,
    name: str,
    region: str,
    phone_number: str,
    user_type_ids: Iterable[int],
) -> None:
    """Сохраняет нового пользователя"""
    try:
        await uow.users.create(
            user_id=user_id,
            name=name,
            region=region,
            phone_number=phone_number,
        )
        for user_type_id in user_type_ids:
            await uow.user_type_users.create(user_id=user_id, user_type_id=user_type_id)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def save_new_feedback(
    uow: UnitOfWork, user_id: int, type: FeedbackType, title: str, text: str
) -> None:
    """Сохраняет новую обратную связь от пользователя"""
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


async def save_new_url(
    uow: UnitOfWork, storage: Storage, slug: str, value: str
) -> UrlDto:
    try:
        url = await uow.urls.create(slug=slug, value=value)
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await storage.refresh_urls()
    return url
