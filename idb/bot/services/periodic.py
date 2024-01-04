from typing import Any

from aiogram import Bot
from aiomisc.service.periodic import PeriodicService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from idb.db.uow import uow_context
from idb.logic.mailing import send_mailings


class PeriodicMailingService(PeriodicService):
    __required__ = ("gap",)
    __dependencies__ = ("bot", "sessionmaker")

    bot: Bot
    sessionmaker: async_sessionmaker[AsyncSession]
    gap: int

    async def callback(self) -> Any:
        async with uow_context(self.sessionmaker) as uow:
            await send_mailings(uow=uow, bot=self.bot, gap=self.gap)
