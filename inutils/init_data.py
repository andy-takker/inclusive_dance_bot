import argparse
import asyncio
import logging
from pathlib import Path
from typing import Any

import yaml
from aiomisc_log import LogFormat, LogLevel, basic_config
from configargparse import ArgumentParser
from pydantic import BaseModel, HttpUrl, ValidationError, field_validator

from idb.db.uow import UnitOfWork
from idb.db.utils import create_engine, create_session_factory
from idb.generals.enums import SubmenuType
from idb.utils.urls import check_slug

log = logging.getLogger(__name__)


class UserTypeSchema(BaseModel):
    id: int
    name: str


class UrlSchema(BaseModel):
    id: int
    slug: str
    value: HttpUrl

    @field_validator("slug")
    @classmethod
    def check_slug(cls, v: str) -> str:
        if not check_slug(v):
            raise ValueError

        return v


class SubmenuSchema(BaseModel):
    id: int
    type: SubmenuType
    weight: int
    button_text: str
    message: str


async def write_urls(uow: UnitOfWork, urls: list[dict[str, Any]]) -> None:
    for u in urls:
        try:
            url = UrlSchema.model_validate(u)
        except ValidationError:
            log.warning("Incorrect url data: %s", u)
        else:
            await uow.urls.upsert(**url.model_dump(mode="json"))


async def write_user_types(uow: UnitOfWork, user_types: list[dict[str, Any]]) -> None:
    for ut in user_types:
        try:
            user_type = UserTypeSchema.model_validate(ut)
        except ValidationError:
            log.warning("Incorrect user type data: %s", ut)
        else:
            await uow.user_types.upsert(**user_type.model_dump(mode="json"))


async def write_submenus(uow: UnitOfWork, submenus: list[dict[str, Any]]) -> None:
    for s in submenus:
        try:
            submenu = SubmenuSchema.model_validate(s)
        except ValidationError:
            log.warning("Incorrect submenu data: %s", s)
        else:
            await uow.submenus.upsert(**submenu.model_dump(mode="json"))


async def write_data(uow: UnitOfWork, filename: Path) -> None:
    log.info("Run init data")
    data = read_data(filename=filename)
    user_types = data.get("user_types")
    urls = data.get("urls")
    submenus = data.get("submenus")
    if urls:
        await write_urls(uow=uow, urls=urls)

    if user_types:
        await write_user_types(uow=uow, user_types=user_types)

    if submenus:
        await write_submenus(uow=uow, submenus=submenus)

    await uow.commit()


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        allow_abbrev=False,
        auto_env_var_prefix="APP_",
        description="Inclusive Dance Bot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    group = parser.add_argument_group("Logging options")
    group.add_argument("--log-level", choices=LogLevel.choices(), default=LogLevel.info)
    group.add_argument(
        "--log-format", choices=LogFormat.choices(), default=LogFormat.color
    )

    group = parser.add_argument_group("PostgreSQL options")
    group.add_argument("--pg-dsn", type=str, required=True)

    group = parser.add_argument_group("Load data params")
    group.add_argument("--init-data-path", type=Path, required=True)

    return parser


def read_data(filename: Path) -> dict[str, Any]:
    with open(filename) as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = get_parser()
    arguments = parser.parse_args()
    if not arguments.init_data_path.exists():
        raise FileNotFoundError
    basic_config(
        level=arguments.log_level,
        log_format=arguments.log_format,
    )
    engine = create_engine(connection_uri=arguments.pg_dsn)
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(sessionmaker=session_factory)
    asyncio.run(write_data(uow=uow, filename=arguments.init_data_path))


if __name__ == "__main__":
    main()
