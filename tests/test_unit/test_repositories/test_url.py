import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Url as UrlDb
from idb.db.repositories.url import UrlRepository
from idb.exceptions import (
    UrlAlreadyExistsError,
    UrlSlugAlreadyExistsError,
)
from idb.generals.models.url import Url
from tests.factories import UrlFactory


async def test_create_url(url_repo: UrlRepository, session: AsyncSession) -> None:
    url = await url_repo.create(
        slug="this_is_my_url",
        value="https://yandex.ru",
    )
    await session.commit()
    saved_url = await session.get(UrlDb, url.id)
    assert url == Url.model_validate(saved_url)


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
    loaded_urls = await url_repo.list()
    assert loaded_urls == tuple()


async def test_get_list(url_repo: UrlRepository) -> None:
    urls = await UrlFactory.create_batch_async(size=5)
    urls.sort(key=lambda x: x.id)
    loaded_urls = await url_repo.list()
    assert loaded_urls == tuple(Url.model_validate(u) for u in urls)
