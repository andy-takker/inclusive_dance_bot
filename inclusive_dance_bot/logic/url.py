from typing import Any

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.exceptions.base import InclusiveDanceError
from inclusive_dance_bot.exceptions.url import UrlSlugAlreadyExistsError
from inclusive_dance_bot.logic.storage import Storage


async def create_url(
    uow: UnitOfWork, storage: Storage, slug: str, value: str
) -> UrlDto:
    """Создает новую ссылку"""
    try:
        url = await uow.urls.create(slug=slug, value=value)
    except UrlSlugAlreadyExistsError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await storage.refresh_urls()
    return url


async def update_url_by_slug(
    uow: UnitOfWork,
    storage: Storage,
    url_slug: str,
    **kwargs: Any,
) -> UrlDto:
    try:
        url = await uow.urls.update_by_slug(url_slug=url_slug, **kwargs)
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await storage.refresh_urls()
    return url


async def delete_url_by_slug(uow: UnitOfWork, storage: Storage, url_slug: str) -> None:
    await uow.urls.delete_by_slug(url_slug=url_slug)
    await uow.commit()
    await storage.refresh_urls()
