from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Url
from src.db.repositories.base import Repository
from src.exceptions import InclusiveDanceError


class UrlRepository(Repository[Url]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Url, session=session)

    async def get_url_list(self) -> Sequence[Url]:
        stmt = select(Url).order_by(Url.slug)
        return (await self._session.scalars(stmt)).all()

    async def create(self, slug: str, value: str, id: int | None = None) -> Url:
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
            return result.one()

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise InclusiveDanceError from err
