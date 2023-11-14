from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Url
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.url import delete_url_by_slug
from tests.factories import UrlFactory


async def test_delete_successful(
    uow: UnitOfWork, storage: Storage, session: AsyncSession
) -> None:
    await UrlFactory.create_async(id=1, slug="new_url")

    await delete_url_by_slug(uow=uow, storage=storage, url_slug="new_url")
    assert await session.get(Url, 1) is None


async def test_delete_unknown_slug(uow: UnitOfWork, storage: Storage) -> None:
    await delete_url_by_slug(uow=uow, storage=storage, url_slug="unknown")
