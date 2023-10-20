from src.db.uow.main import UnitOfWork
from src.enums import FeedbackType
from src.middlewares.cache import CacheStorage


async def save_new_user(
    uow: UnitOfWork,
    user_id: int,
    name: str,
    region: str,
    phone_number: str,
    user_type_ids: list[int],
) -> None:
    """Сохраняет нового пользователя"""
    await uow.users.create(
        user_id=user_id,
        name=name,
        region=region,
        phone_number=phone_number,
    )
    for user_type_id in user_type_ids:
        await uow.users.add_user_type_to_user(
            user_id=user_id, user_type_id=user_type_id
        )
    await uow.commit()


async def update_url_cache(
    uow: UnitOfWork,
    cache: CacheStorage,
) -> None:
    """Обновляет кэш ссылок для сообщений"""
    urls = await uow.urls.get_url_list()
    cache.clear()
    for url in urls:
        cache.set(url.slug, url.value)


async def save_new_feedback(
    uow: UnitOfWork, user_id: int, feedback_type: FeedbackType, title: str, text: str
) -> None:
    """Сохраняет новую обратную связь от пользователя"""
