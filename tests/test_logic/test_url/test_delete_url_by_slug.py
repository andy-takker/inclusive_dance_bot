from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Url
from idb.db.uow import UnitOfWork
from idb.logic.url import delete_url_by_slug
from idb.utils.cache import MemoryCache
from tests.factories import UrlFactory


async def test_delete_successful(
    uow: UnitOfWork, memory_cache: MemoryCache, session: AsyncSession
) -> None:
    await UrlFactory.create_async(id=1, slug="new_url")

    await delete_url_by_slug(uow=uow, cache=memory_cache, url_slug="new_url")
    assert await session.get(Url, 1) is None


async def test_delete_unknown_slug(uow: UnitOfWork, memory_cache: MemoryCache) -> None:
    await delete_url_by_slug(uow=uow, cache=memory_cache, url_slug="unknown")
