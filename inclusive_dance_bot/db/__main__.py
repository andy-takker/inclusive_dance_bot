import argparse
import logging
import os

from alembic.config import CommandLine

from inclusive_dance_bot.db.utils import make_alembic_config

DEFAULT_PG_URL = "postgresql://user:secret@localhost/inclusive_dance_bot"


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        "--pg-url",
        default=os.getenv("POSTGRES_URL", DEFAULT_PG_URL),
        help="Database URL [env var: POSTGRES_URL]",
    )

    options = alembic.parser.parse_args()
    if "cmd" not in options:
        alembic.parser.error("too few arguments")
        exit(128)
    else:
        config = make_alembic_config(options)
        alembic.run_cmd(config, options)
        exit()


if __name__ == "__main__":
    main()
