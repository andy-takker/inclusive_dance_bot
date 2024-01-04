from typing import Any

from idb.db.uow import UnitOfWork
from idb.exceptions.base import InclusiveDanceError
from idb.exceptions.url import UrlSlugAlreadyExistsError
from idb.generals.models.url import Url
from idb.utils.cache import AbstractBotCache


async def create_url(
    uow: UnitOfWork, cache: AbstractBotCache, slug: str, value: str
) -> Url:
    """Создает новую ссылку"""
    try:
        url = await uow.urls.create(slug=slug, value=value)
    except UrlSlugAlreadyExistsError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await cache.update_url(slug=url.slug, url=url)
    return url


async def update_url_by_slug(
    uow: UnitOfWork,
    cache: AbstractBotCache,
    url_slug: str,
    **kwargs: Any,
) -> Url:
    try:
        url = await uow.urls.update_by_slug(url_slug=url_slug, **kwargs)
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    if url.slug != url_slug:
        await cache.update_url(slug=url_slug, url=None)
    await cache.update_url(slug=url.slug, url=url)
    return url


async def delete_url_by_slug(
    uow: UnitOfWork, cache: AbstractBotCache, url_slug: str
) -> None:
    await uow.urls.delete_by_slug(url_slug=url_slug)
    await uow.commit()
    await cache.update_url(slug=url_slug, url=None)
