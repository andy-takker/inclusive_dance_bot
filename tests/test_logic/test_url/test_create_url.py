import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Url as UrlDb
from idb.db.uow import UnitOfWork
from idb.exceptions.url import UrlSlugAlreadyExistsError
from idb.generals.models.url import Url
from idb.logic.url import create_url
from idb.utils.cache import MemoryCache
from tests.factories import UrlFactory


async def test_create_successful(
    uow: UnitOfWork,
    memory_cache: MemoryCache,
    session: AsyncSession,
) -> None:
    slug = "new_url_slug"
    value = "https://example.com"

    url = await create_url(uow=uow, cache=memory_cache, slug=slug, value=value)

    loaded_url = await session.get(UrlDb, url.id)
    assert Url.model_validate(loaded_url) == url


async def test_error_url_slug_already_exists(
    uow: UnitOfWork,
    memory_cache: MemoryCache,
) -> None:
    url = await UrlFactory.create_async()
    with pytest.raises(UrlSlugAlreadyExistsError):
        await create_url(uow=uow, cache=memory_cache, slug=url.slug, value="somevalue")
