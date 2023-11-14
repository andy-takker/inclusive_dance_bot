import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Url
from inclusive_dance_bot.db.repositories.url import UrlRepository
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.exceptions import (
    UrlAlreadyExistsError,
    UrlSlugAlreadyExistsError,
)
from tests.factories import UrlFactory


async def test_create_url(url_repo: UrlRepository, session: AsyncSession) -> None:
    url = await url_repo.create(
        slug="this_is_my_url",
        value="https://yandex.ru",
    )
    await session.commit()
    saved_url = await session.get(Url, url.id)
    assert url == UrlDto.from_orm(saved_url)


async def test_invalid_double_create_by_id(
    url_repo: UrlRepository, session: AsyncSession
) -> None:
    await url_repo.create(
        id=1,
        slug="this_is_my_url",
        value="https://yandex.ru",
    )
    await session.commit()
    with pytest.raises(UrlAlreadyExistsError):
        await url_repo.create(
            id=1,
            slug="this_is_my_other_url",
            value="https://yandex.ru",
        )


async def test_invalid_double_create_by_slug(
    url_repo: UrlRepository,
) -> None:
    await url_repo.create(
        slug="this_is_url",
        value="https://ya.ru",
    )
    with pytest.raises(UrlSlugAlreadyExistsError):
        await url_repo.create(
            slug="this_is_url",
            value="httsp://best.ru",
        )


async def test_get_list_empty(url_repo: UrlRepository) -> None:
    loaded_urls = await url_repo.get_list()
    assert loaded_urls == tuple()


async def test_get_list(url_repo: UrlRepository) -> None:
    urls = await UrlFactory.create_batch_async(size=5)

    loaded_urls = await url_repo.get_list()
    assert set(loaded_urls) == {UrlDto.from_orm(u) for u in urls}
