from typing import Any, NoReturn

from sqlalchemy import ScalarResult, delete, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.models import Url
from inclusive_dance_bot.db.repositories.base import Repository
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.exceptions import (
    InclusiveDanceError,
    UrlAlreadyExistsError,
    UrlSlugAlreadyExistsError,
)


class UrlRepository(Repository[Url]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Url, session=session)

    async def create(self, slug: str, value: str, id: int | None = None) -> UrlDto:
        data: dict[str, str | int] = dict(slug=slug, value=value)
        if id is not None:
            data["id"] = id
        stmt = insert(Url).values(**data).returning(Url)
        try:
            result: ScalarResult[Url] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        else:
            await self._session.flush()
            return UrlDto.from_orm(result.one())

    async def update_by_slug(self, url_slug: str, **kwargs: Any) -> UrlDto:
        try:
            url = await self._update(Url.slug == url_slug, **kwargs)
        except IntegrityError as e:
            self._raise_error(e)
        return UrlDto.from_orm(url)

    async def delete_by_slug(self, url_slug: str) -> None:
        stmt = delete(Url).where(Url.slug == url_slug)
        await self._session.execute(stmt)

    async def get_all_urls(self) -> tuple[UrlDto, ...]:
        stmt = select(Url).order_by(Url.slug)
        objs = (await self._session.scalars(stmt)).all()
        return tuple(UrlDto.from_orm(obj) for obj in objs)

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__url":
            raise UrlAlreadyExistsError from e
        if constraint == "uq__url__slug":
            raise UrlSlugAlreadyExistsError from e
        raise InclusiveDanceError from e
