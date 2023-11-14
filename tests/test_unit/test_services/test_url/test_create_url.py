import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Url
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.exceptions.url import UrlSlugAlreadyExistsError
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.url import create_url
from tests.factories import UrlFactory


async def test_create_successful(
    uow: UnitOfWork,
    storage: Storage,
    session: AsyncSession,
) -> None:
    slug = "new_url_slug"
    value = "https://example.com"

    url = await create_url(uow=uow, storage=storage, slug=slug, value=value)

    loaded_url = await session.get(Url, url.id)
    assert UrlDto.from_orm(loaded_url) == url


async def test_error_url_slug_already_exists(uow: UnitOfWork, storage: Storage) -> None:
    url = await UrlFactory.create_async()
    with pytest.raises(UrlSlugAlreadyExistsError):
        await create_url(uow=uow, storage=storage, slug=url.slug, value="somevalue")
