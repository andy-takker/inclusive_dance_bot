import argparse
import json

from aiogram.enums import ParseMode
from aiomisc_log import LogFormat, LogLevel
from configargparse import ArgumentParser


def int_list(s: str) -> list[int]:
    try:
        value = json.loads(s)
        if not isinstance(value, list):
            raise ValueError
        if not all(map(lambda x: isinstance(x, int), value)):
            raise ValueError
        return value
    except (json.JSONDecodeError, ValueError):
        raise ValueError("This is not list of integers")


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        allow_abbrev=False,
        auto_env_var_prefix="APP_",
        description="Inclusive Dance Bot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-D", "--debug", action="store_true")
    parser.add_argument(
        "-s",
        "--pool-size",
        type=int,
        default=6,
        help="Thread pool size",
    )

    group = parser.add_argument_group("Logging options")
    group.add_argument("--log-level", choices=LogLevel.choices(), default=LogLevel.info)
    group.add_argument(
        "--log-format", choices=LogFormat.choices(), default=LogFormat.color
    )

    group = parser.add_argument_group("Telegram Bot options")
    group.add_argument("--telegram-bot-token", required=True)
    group.add_argument("--telegram-bot-admin-ids", type=int_list, default=[])
    group.add_argument(
        "--telegram-parse-mode",
        type=ParseMode,
        choices=tuple(ParseMode._member_names_),
        default=ParseMode.HTML,
    )

    group.add_argument("--telegram-periodic-interval", type=int, default=5 * 60)
    group.add_argument("--telegram-mailing-gap", type=int, default=2 * 60)

    group = parser.add_argument_group("PostgreSQL options")
    group.add_argument("--pg-dsn", type=str, required=True)

    group = parser.add_argument_group("Redis options")
    group.add_argument("--redis-dsn", type=str, required=True)

    return parser
