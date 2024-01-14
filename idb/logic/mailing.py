import logging
from datetime import UTC, datetime
from typing import Any

import pytz
from aiogram import Bot
from aiogram.enums import ParseMode

from idb.db.uow import UnitOfWork
from idb.generals.enums import MailingStatus
from idb.generals.models.mailing import Mailing

log = logging.getLogger(__name__)


async def send_mailings(
    uow: UnitOfWork,
    bot: Bot,
    gap: int,
) -> None:
    new_mailings = await uow.mailings.get_new_mailings(
        gap=gap, now=datetime.now(tz=UTC)
    )
    log.info("Found %d new mailings", len(new_mailings))
    for mailing in new_mailings:
        await process_new_mailing(uow=uow, bot=bot, mailing=mailing)


async def process_new_mailing(uow: UnitOfWork, bot: Bot, mailing: Mailing) -> None:
    log.info("Start process mailing_id=%s", mailing.id)
    users = await uow.users.get_list_by_user_types(user_types=mailing.user_types)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.id,
                text=f"{mailing.title}\n\n{mailing.content}",
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            log.exception("Occured something")
    now = datetime.now(tz=pytz.utc)
    await uow.mailings.update_by_id(
        mailing_id=mailing.id,
        status=MailingStatus.SENT,
        sent_at=now,
    )
    await uow.commit()


async def save_mailing(
    uow: UnitOfWork,
    bot: Bot,
    author_id: int,
    title: str,
    content: str,
    scheduled_at: datetime | None,
    user_type_ids: list[int],
) -> None:
    mailing = await uow.mailings.create(
        author_id=author_id,
        title=title,
        content=content,
        scheduled_at=scheduled_at,
        status=MailingStatus.SCHEDULED,
        sent_at=None,
    )
    for user_type_id in user_type_ids:
        await uow.mailings.create_mailing_user_type(
            mailing_id=mailing.id, user_type_id=user_type_id
        )
    await uow.commit()
    if scheduled_at is not None:
        return
    mailing = await uow.mailings.get_by_id(mailing_id=mailing.id)
    await process_new_mailing(uow=uow, bot=bot, mailing=mailing)


async def update_mailing_by_id(
    uow: UnitOfWork, mailing_id: int, **kwargs: Any
) -> Mailing:
    mailing = await uow.mailings.update_by_id(mailing_id=mailing_id, **kwargs)
    await uow.commit()
    return mailing
