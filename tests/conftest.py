import asyncio
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from inclusive_dance_bot.db.base import Base
from inclusive_dance_bot.db.utils import (
    create_engine,
    create_session_factory,
    make_alembic_config,
)
from tests.factories import FACTORIES
from tests.utils import prepare_new_database, run_async_migrations

TABLES_FOR_TRUNCATE = (
    "submenu",
    "url",
    "users",
    "user_type",
    "user_type_user",
    "feedback",
)

PROJECT_PATH = Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_name():
    default = "test_pgdb"
    return os.getenv("APP_PG_DB_NAME", default)


@pytest.fixture(scope="session")
def pg_dsn(localhost, db_name: str) -> str:
    default = f"postgresql+asyncpg://pguser:pguser@{localhost}:5432/{db_name}"
    return os.getenv("APP_PG_DSN", default)


@pytest.fixture(scope="session")
def base_pg_dsn(localhost) -> str:
    default = f"postgresql+asyncpg://pguser:pguser@{localhost}:5432/postgres"
    return os.getenv("APP_BASE_PG_DSN", default)


@pytest.fixture(scope="session")
def alembic_config(pg_dsn: str) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=pg_dsn,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture(scope="session")
async def async_engine(
    alembic_config: AlembicConfig,
    base_pg_dsn: str,
    pg_dsn: str,
    db_name: str,
) -> AsyncEngine:
    await prepare_new_database(base_pg_dsn=base_pg_dsn, db_name=db_name)
    await run_async_migrations(alembic_config, Base.metadata, "head")
    engine = create_engine(pg_dsn)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="session")
def sessionmaker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    yield create_session_factory(engine=async_engine)


@pytest.fixture(autouse=True)
async def session(
    sessionmaker: async_sessionmaker[AsyncSession], async_engine: AsyncEngine
) -> AsyncSession:
    try:
        session: AsyncSession = sessionmaker()
        for factory in FACTORIES:
            factory.__async_session__ = session
        yield session
    finally:
        await session.close()
        await _clear_db(async_engine)


async def _clear_db(engine: AsyncEngine) -> None:
    tables = ", ".join(TABLES_FOR_TRUNCATE)
    sql = f"TRUNCATE TABLE {tables} CASCADE"
    async with engine.connect() as conn:
        await conn.execute(text(sql))
        await conn.commit()
