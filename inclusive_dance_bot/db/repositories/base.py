from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.base import Base
from inclusive_dance_bot.exceptions import EntityNotFoundError

Model = TypeVar("Model", bound=Base)


class Repository(ABC, Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def _get_by_id_or_none(self, obj_id: int) -> Model | None:
        return await self._session.get(self._model, obj_id)

    async def _get_by_id(self, obj_id: int) -> Model:
        return await self._session.get_one(self._model, obj_id)

    async def _update(self, *args: Any, **kwargs: Any) -> Model:
        query = update(self._model).where(*args).values(**kwargs).returning(self._model)
        result = await self._session.scalars(select(self._model).from_statement(query))
        try:
            obj = result.one()
            await self._session.flush(obj)
        except NoResultFound as e:
            raise EntityNotFoundError from e
        await self._session.refresh(obj)
        return obj
