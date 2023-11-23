import os
from argparse import Namespace
from pathlib import Path
from typing import Any

from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import inclusive_dance_bot

PROJECT_PATH = Path(inclusive_dance_bot.__file__).parent.parent.resolve()


def create_engine(connection_uri: str, **engine_kwargs: Any) -> AsyncEngine:
    return create_async_engine(url=connection_uri, **engine_kwargs, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def make_alembic_config(cmd_opts: Namespace, base_path: Path = PROJECT_PATH) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = str(base_path / "inclusive_dance_bot/db" / cmd_opts.config)

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise ValueError
    print(alembic_location)
    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(base_path / alembic_location))

    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    config.attributes["configure_logger"] = False

    return config
