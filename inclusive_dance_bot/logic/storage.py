from collections.abc import Iterator, MutableMapping
from typing import Any

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import SubmenuDto, UrlDto, UserTypeDto
from inclusive_dance_bot.enums import StorageType


class CacheStorage(MutableMapping):
    def __init__(self) -> None:
        self.__storage: dict[str, Any] = {}

    def __getitem__(self, key: str) -> Any:
        return self.__storage[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__storage[key] = value

    def __delitem__(self, key: str) -> None:
        del self.__storage[key]

    def __len__(self) -> int:
        return len(self.__storage)

    def __iter__(self) -> Iterator:
        return iter(self.__storage)

    def __repr__(self) -> str:
        return repr(self.__storage)

    def clear(self) -> None:
        self.__storage.clear()


class Storage:
    _uow: UnitOfWork
    _cache: CacheStorage

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
        self._cache = CacheStorage()

    async def get_urls(self) -> dict[str, UrlDto]:
        if StorageType.URL not in self._cache:
            self._cache[StorageType.URL] = {
                url.slug: url for url in await self._uow.urls.get_list()
            }
        return self._cache[StorageType.URL]

    async def get_url_by_slug(self, slug: str) -> UrlDto:
        urls = await self.get_urls()
        return urls[slug]

    async def get_user_types(self) -> dict[int, UserTypeDto]:
        if StorageType.USER_TYPE not in self._cache:
            self._cache[StorageType.USER_TYPE] = {
                ut.id: ut for ut in await self._uow.user_types.get_list()
            }
        return self._cache[StorageType.USER_TYPE]

    async def get_submenus(self) -> dict[int, SubmenuDto]:
        if StorageType.SUBMENU not in self._cache:
            self._cache[StorageType.SUBMENU] = {
                e.id: e for e in await self._uow.submenus.get_list()
            }
        return self._cache[StorageType.SUBMENU]

    async def get_submenu_by_id(self, submenu_id: int) -> SubmenuDto:
        submenus = await self.get_submenus()
        return submenus[submenu_id]

    async def refresh_all(self) -> None:
        self._cache.clear()
        await self.get_urls()
        await self.get_submenus()
        await self.get_user_types()

    async def refresh_urls(self) -> None:
        if StorageType.URL in self._cache:
            del self._cache[StorageType.URL]
        await self.get_urls()

    async def refresh_submenus(self) -> None:
        if StorageType.SUBMENU in self._cache:
            del self._cache[StorageType.SUBMENU]
        await self.get_submenus()
