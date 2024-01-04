import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.uow import UnitOfWork
from idb.exceptions.url import (
    UrlNotFoundError,
    UrlSlugAlreadyExistsError,
)
from idb.generals.models.url import Url
from idb.logic.url import update_url_by_slug
from idb.utils.cache import MemoryCache
from tests.factories import UrlFactory


async def test_update_successful(
    uow: UnitOfWork, memory_cache: MemoryCache, session: AsyncSession
) -> None:
    url = await UrlFactory.create_async(slug="slug")
    updated_url = await update_url_by_slug(
        uow=uow, cache=memory_cache, url_slug="slug", value="https://vk.com"
    )

    await session.refresh(url)
    assert url.value == "https://vk.com"

    assert updated_url == Url.model_validate(url)


async def test_error_url_not_found(uow: UnitOfWork, memory_cache: MemoryCache) -> None:
    with pytest.raises(UrlNotFoundError):
        await update_url_by_slug(
            uow=uow, cache=memory_cache, url_slug="unknown", value=""
        )


async def test_error_url_slug_already_exists(
    uow: UnitOfWork, memory_cache: MemoryCache
) -> None:
    await UrlFactory.create_async(slug="first_url")
    await UrlFactory.create_async(slug="second_url")
    with pytest.raises(UrlSlugAlreadyExistsError):
        await update_url_by_slug(
            uow=uow,
            cache=memory_cache,
            url_slug="second_url",
            slug="first_url",
        )
