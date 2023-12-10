import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config

from inclusive_dance_bot.arguments import get_parser
from inclusive_dance_bot.deps import config_deps
from inclusive_dance_bot.services.bot import AiogramBotService
from inclusive_dance_bot.services.periodic import PeriodicMailingService

log = logging.getLogger(__name__)


def main() -> None:
    parser = get_parser()
    arguments = parser.parse_args()
    basic_config(
        log_format=arguments.log_level,
        level=arguments.log_format,
    )
    config_deps(arguments=arguments)
    services: list[Service] = [
        AiogramBotService(
            debug=arguments.debug,
            redis_dsn=arguments.redis_dsn,
            telegram_bot_admin_ids=arguments.telegram_bot_admin_ids,
        ),
        PeriodicMailingService(
            interval=arguments.telegram_periodic_interval,
            delay=0,
            gap=arguments.telegram_mailing_gap,
        ),
    ]
    with entrypoint(
        *services,
    ) as loop:
        log.info("Entrypoint started")
        loop.run_forever()


if __name__ == "__main__":
    main()
