from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.logic.storage import Storage
from tests.factories import UrlFactory


def test_initial_storage_is_empty(storage: Storage) -> None:
    assert len(storage._cache) == 0


async def test_get_urls(storage: Storage) -> None:
    first_url = await UrlFactory.create_async()
    second_url = await UrlFactory.create_async()
    urls = await storage.get_urls()
    assert urls == {
        first_url.slug: UrlDto.from_orm(first_url),
        second_url.slug: UrlDto.from_orm(second_url),
    }


async def test_cache_get_urls(storage: Storage, session: AsyncSession) -> None:
    first_url = await UrlFactory.create_async()
    second_url = await UrlFactory.create_async()
    await storage.get_urls()
    await session.delete(second_url)
    await session.delete(first_url)
    await session.commit()
    urls = await storage.get_urls()
    assert urls == {
        first_url.slug: UrlDto.from_orm(first_url),
        second_url.slug: UrlDto.from_orm(second_url),
    }


async def test_get_url_by_slug(storage: Storage) -> None:
    new_url = await UrlFactory.create_async(slug="my_url")
    url = await storage.get_url_by_slug("my_url")
    assert UrlDto.from_orm(new_url) == url


async def test_cache_get_url_by_slug(storage: Storage, session: AsyncSession) -> None:
    url = await UrlFactory.create_async(slug="my_slug")
    await storage.get_url_by_slug("my_slug")

    await session.delete(url)

    cached_url = await storage.get_url_by_slug("my_slug")
    assert cached_url.slug == "my_slug"


async def test_get_user_types(storage: Storage) -> None:
    pass


async def test_cache_get_user_types(storage: Storage, session: AsyncSession) -> None:
    pass


async def test_get_submenus(storage: Storage) -> None:
    pass


async def test_cache_get_submenus(storage: Storage, session: AsyncSession) -> None:
    pass


async def test_refresh_all(storage: Storage, session: AsyncSession) -> None:
    pass


async def test_refresh_urls(storage: Storage, session: AsyncSession) -> None:
    pass
