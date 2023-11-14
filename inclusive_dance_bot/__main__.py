import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config

from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.deps import config_deps
from inclusive_dance_bot.services.bot import AiogramBotService
from inclusive_dance_bot.services.periodic import PeriodicMailingService

log = logging.getLogger(__name__)


def main() -> None:
    settings = Settings()
    basic_config()
    config_deps(app_settings=settings)
    services: list[Service] = [
        AiogramBotService(),
        PeriodicMailingService(
            interval=settings.PERIODIC_INTERVAL,
            delay=0,
            gap=settings.MAILING_GAP,
        ),
    ]
    with entrypoint(
        *services,
    ) as loop:
        log.info("Entrypoint started")
        loop.run_forever()
