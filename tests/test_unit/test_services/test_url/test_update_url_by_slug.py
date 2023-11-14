import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.exceptions.url import (
    UrlNotFoundError,
    UrlSlugAlreadyExistsError,
)
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.url import update_url_by_slug
from tests.factories import UrlFactory


async def test_update_successful(
    uow: UnitOfWork, storage: Storage, session: AsyncSession
) -> None:
    url = await UrlFactory.create_async(slug="slug")
    updated_url = await update_url_by_slug(
        uow=uow, storage=storage, url_slug="slug", value="https://vk.com"
    )

    await session.refresh(url)
    assert url.value == "https://vk.com"

    assert updated_url == UrlDto.from_orm(url)


async def test_error_url_not_found(uow: UnitOfWork, storage: Storage) -> None:
    with pytest.raises(UrlNotFoundError):
        await update_url_by_slug(uow=uow, storage=storage, url_slug="unknown", value="")


async def test_error_url_slug_already_exists(uow: UnitOfWork, storage: Storage) -> None:
    await UrlFactory.create_async(slug="first_url")
    await UrlFactory.create_async(slug="second_url")
    with pytest.raises(UrlSlugAlreadyExistsError):
        await update_url_by_slug(
            uow=uow,
            storage=storage,
            url_slug="second_url",
            slug="first_url",
        )
