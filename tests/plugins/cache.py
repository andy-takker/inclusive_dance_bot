import os

import pytest

from idb.utils.cache import KeyBuilder, MemoryCache, RedisCache


@pytest.fixture
async def memory_cache() -> MemoryCache:
    return MemoryCache()


@pytest.fixture(scope="session")
def redis_dsn(localhost) -> str:
    default = f"redis://{localhost}:6379/0"
    return os.getenv("APP_REDIS_DSN", default)


@pytest.fixture
async def redis_cache(redis_dsn: str) -> RedisCache:
    cache = RedisCache.from_url(url=redis_dsn, key_builder=KeyBuilder())
    try:
        await cache.flushall()
        yield cache
    finally:
        await cache.flushall()
        await cache.close()
