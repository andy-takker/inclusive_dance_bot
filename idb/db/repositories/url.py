from typing import Any, NoReturn

from sqlalchemy import ScalarResult, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Url as UrlDb
from idb.db.repositories.base import Repository
from idb.exceptions import (
    InclusiveDanceError,
    UrlAlreadyExistsError,
    UrlSlugAlreadyExistsError,
)
from idb.exceptions.base import EntityNotFoundError
from idb.exceptions.url import UrlNotFoundError
from idb.generals.models.url import Url


class UrlRepository(Repository[UrlDb]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=UrlDb, session=session)

    async def create(self, slug: str, value: str, id: int | None = None) -> Url:
        data: dict[str, str | int] = dict(slug=slug, value=value)
        if id is not None:
            data["id"] = id
        stmt = insert(UrlDb).values(**data).returning(UrlDb)
        try:
            result: ScalarResult[UrlDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return Url.model_validate(result.one())

    async def update_by_slug(self, url_slug: str, **kwargs: Any) -> Url:
        try:
            url = await self._update(UrlDb.slug == url_slug, **kwargs)
        except EntityNotFoundError as e:
            raise UrlNotFoundError from e
        except IntegrityError as e:
            self._raise_error(e)
        return Url.model_validate(url)

    async def delete_by_slug(self, url_slug: str) -> None:
        stmt = delete(UrlDb).where(UrlDb.slug == url_slug)
        await self._session.execute(stmt)

    async def list(self) -> tuple[Url, ...]:
        stmt = select(UrlDb).order_by(UrlDb.id)
        objs = (await self._session.scalars(stmt)).all()
        return tuple(Url.model_validate(obj) for obj in objs)

    async def upsert(self, *, id: int, slug: str, value: str) -> Url:
        stmt = (
            insert(UrlDb)
            .values(id=id, slug=slug, value=value)
            .on_conflict_do_update(
                index_elements=[UrlDb.slug],
                set_={
                    "id": id,
                    "slug": slug,
                    "value": value,
                },
            )
            .returning(UrlDb)
        )
        try:
            result: ScalarResult[UrlDb] = await self._session.scalars(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        await self._session.flush()
        return Url.model_validate(result.one())

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "pk__url":
            raise UrlAlreadyExistsError from e
        if constraint == "uq__url__slug":
            raise UrlSlugAlreadyExistsError from e
        raise InclusiveDanceError from e
