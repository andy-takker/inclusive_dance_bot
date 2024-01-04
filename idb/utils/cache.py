import json
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Callable, Mapping, MutableMapping
from dataclasses import asdict, dataclass
from enum import StrEnum, unique
from typing import Any

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from idb.db.uow import UnitOfWork
from idb.generals.models.submenu import Submenu
from idb.generals.models.url import Url
from idb.generals.models.user_type import UserType

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


@unique
class CacheType(StrEnum):
    URL = "URL"
    USER_TYPE = "USER_TYPE"
    SUBMENU = "SUBMENU"


@dataclass(frozen=True)
class CacheKey:
    entity_type: CacheType
    entity_id: str


class KeyBuilder:
    def __init__(self, prefix: str = "bot", sep: str = "__") -> None:
        self._sep = sep
        self._prefix = prefix

    def build_key(self, group: CacheType, entity_id: str | int) -> str:
        return self._sep.join([self._prefix, group, str(entity_id)])

    def build_group_pattern(self, group: CacheType) -> str:
        return self._sep.join([self._prefix, group]) + "*"

    def parse_id(self, dumped_key: str) -> str:
        return dumped_key.split(self._sep)[-1]


class AbstractBotCache(ABC):
    @abstractmethod
    async def get_urls(self) -> Mapping[str, Url]:
        pass

    @abstractmethod
    async def get_url_by_slug(self, slug: str) -> Url:
        pass

    @abstractmethod
    async def get_submenus(self) -> Mapping[int, Submenu]:
        pass

    @abstractmethod
    async def get_submenu_by_id(self, id_: int) -> Submenu:
        pass

    @abstractmethod
    async def get_user_types(self) -> Mapping[int, UserType]:
        pass

    @abstractmethod
    async def update_url(self, slug: str, url: Url | None) -> None:
        pass

    @abstractmethod
    async def update_submenu(self, id_: int, submenu: Submenu | None) -> None:
        pass

    @abstractmethod
    async def load_cache(self, uow: UnitOfWork) -> None:
        pass


class RedisCache(AbstractBotCache):
    _redis: Redis
    _key_builder: KeyBuilder
    _json_dumps: _JsonDumps
    _json_loads: _JsonLoads

    def __init__(
        self,
        redis: Redis,
        key_builder: KeyBuilder,
        json_dumps: _JsonDumps = json.dumps,
        json_loads: _JsonLoads = json.loads,
    ) -> None:
        self._redis = redis
        self._key_builder = key_builder
        self._json_dumps = json_dumps
        self._json_loads = json_loads

    @classmethod
    def from_url(
        cls, url: str, connection_kwargs: dict[str, Any] | None = None, **kwargs: Any
    ) -> "RedisCache":
        if connection_kwargs is None:
            connection_kwargs = {}
        pool = ConnectionPool.from_url(url, **connection_kwargs)
        redis = Redis(connection_pool=pool)
        return cls(redis=redis, **kwargs)

    async def close(self) -> None:
        await self._redis.close()

    async def flushall(self) -> None:
        await self._redis.flushall()

    async def _set_data(self, group: CacheType, entity_id: int | str, obj: Any) -> None:
        key = self._key_builder.build_key(group, entity_id)
        if obj is None:
            await self._redis.delete(key)
        else:
            await self._redis.set(obj, self._json_dumps(asdict(obj)))

    async def _get_data(
        self, group: CacheType, entity_id: int | str
    ) -> Mapping[str, Any]:
        key = self._key_builder.build_key(group, entity_id)
        return self._json_loads(self._redis.get(key))

    async def load_cache(self, uow: UnitOfWork) -> None:
        for submenu in await uow.submenus.list():
            await self._set_data(CacheType.SUBMENU, submenu.id, submenu)

        for url in await uow.urls.list():
            await self._set_data(CacheType.URL, url.slug, url)

        for ut in await uow.user_types.list():
            await self._set_data(CacheType.USER_TYPE, ut.id, ut)

    async def _get_group_iter(
        self, group: CacheType
    ) -> AsyncGenerator[tuple[str, Any], None]:
        pattern = self._key_builder.build_group_pattern(group)
        async for key in self._redis.scan_iter(pattern):
            yield key, await self._redis.get(key)

    async def get_submenus(self) -> Mapping[int, Submenu]:
        submenus: dict[int, Submenu] = {}
        async for key, value in self._get_group_iter(CacheType.SUBMENU):
            submenus[int(key)] = Submenu(**self._json_loads(value))
        return submenus

    async def get_urls(self) -> Mapping[str, Url]:
        urls: dict[str, Url] = {}
        async for key, value in self._get_group_iter(CacheType.URL):
            urls[key] = Url(**self._json_loads(value))
        return urls

    async def get_user_types(self) -> Mapping[int, UserType]:
        user_types: dict[int, UserType] = {}
        async for key, value in self._get_group_iter(CacheType.USER_TYPE):
            user_types[int(key)] = UserType(**self._json_loads(value))
        return user_types

    async def update_submenu(self, id_: int, submenu: Submenu | None) -> None:
        await self._set_data(group=CacheType.SUBMENU, entity_id=id_, obj=submenu)

    async def update_url(self, slug: str, url: Url | None) -> None:
        await self._set_data(group=CacheType.URL, entity_id=slug, obj=url)

    async def get_submenu_by_id(self, id_: int) -> Submenu:
        data = await self._get_data(group=CacheType.SUBMENU, entity_id=id_)
        return Submenu(**data)

    async def get_url_by_slug(self, slug: str) -> Url:
        data = await self._get_data(group=CacheType.URL, entity_id=slug)
        return Url(**data)


class MemoryCache(AbstractBotCache):
    def __init__(self) -> None:
        self._urls: MutableMapping[str, Url] = {}
        self._submenus: MutableMapping[int, Submenu] = {}
        self._user_types: MutableMapping[int, UserType] = {}

    async def load_cache(self, uow: UnitOfWork) -> None:
        urls = await uow.urls.list()
        self._urls = {url.slug: url for url in urls}

        submenus = await uow.submenus.list()
        self._submenus = {submenu.id: submenu for submenu in submenus}

        user_types = await uow.user_types.list()
        self._user_types = {ut.id: ut for ut in user_types}

    async def get_urls(self) -> Mapping[str, Url]:
        return self._urls

    async def get_url_by_slug(self, slug: str) -> Url:
        return self._urls[slug]

    async def get_submenus(self) -> Mapping[int, Submenu]:
        return self._submenus

    async def get_submenu_by_id(self, id_: int) -> Submenu:
        return self._submenus[id_]

    async def get_user_types(self) -> Mapping[int, UserType]:
        return self._user_types

    async def update_url(self, slug: str, url: Url | None) -> None:
        if url is None and slug in self._urls:
            del self._urls[slug]
        elif url is not None:
            self._urls[slug] = url

    async def update_submenu(self, id_: int, submenu: Submenu | None) -> None:
        if submenu is None and id_ in self._submenus:
            del self._submenus[id_]
        elif submenu is not None:
            self._submenus[id_] = submenu
