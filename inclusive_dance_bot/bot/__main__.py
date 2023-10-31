import asyncio
import logging

from inclusive_dance_bot.bot.factory import get_bot, get_dispatcher
from inclusive_dance_bot.bot.ui_commands import set_ui_commands
from inclusive_dance_bot.config import Settings

log = logging.getLogger(__name__)


async def start_bot(settings: Settings) -> None:
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format="%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S %d.%m.%Y",
    )
    log.info("Init bot")
    if settings.TELEGRAM_BOT_TOKEN.get_secret_value() == "default":
        raise ValueError("You should set env TELEGRAM_BOT_TOKEN")

    bot = get_bot(settings=settings)
    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    async with get_dispatcher(settings=settings) as dp:
        await dp.start_polling(bot)
    log.info("Stopped")


def main() -> None:
    settings = Settings()
    asyncio.run(start_bot(settings=settings))


if __name__ == "__main__":
    main()
