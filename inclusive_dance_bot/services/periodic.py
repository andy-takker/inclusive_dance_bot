from typing import Any

from aiogram import Bot
from aiomisc.service.periodic import PeriodicService

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.mailing import send_mailings


class PeriodicMailingService(PeriodicService):
    __required__ = ("gap",)
    __dependencies__ = ("bot", "uow")

    bot: Bot
    uow: UnitOfWork
    gap: int

    async def callback(self) -> Any:
        async with self.uow:
            await send_mailings(uow=self.uow, bot=self.bot, gap=self.gap)
