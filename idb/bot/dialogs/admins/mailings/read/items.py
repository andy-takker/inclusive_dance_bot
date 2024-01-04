from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, List

from idb.bot.dialogs.admins.states import MailingsSG
from idb.bot.dialogs.utils import sync_scroll
from idb.bot.dialogs.utils.buttons import BACK
from idb.db.uow import UnitOfWork

MAILING_TEMPLATE = """\
[{pos}] {item.title}
Создано: {item.created_at:%H:%M %d.%m.%Y}
Статус: {item.status}
"""


async def get_mailings_data(
    uow: UnitOfWork, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    if dialog_manager.dialog_data.get("is_sent"):
        mailings = await uow.mailings.get_archive_mailings()
    else:
        mailings = await uow.mailings.get_new_mailings()
    return {"mailings": mailings}


async def open_mailing(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, mailing_id: int
) -> None:
    dialog_manager.dialog_data["mailing_id"] = mailing_id
    await dialog_manager.next()


window = Window(
    Const("Запланированные рассылки\n", when=~F["is_sent"]),
    Const("Архив рассылок\n", when=F["is_sent"]),
    List(
        Format(MAILING_TEMPLATE),
        items="mailings",
        id="scroll_message_mailings",
        page_size=10,
    ),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_mailing",
            item_id_getter=lambda x: x.id,
            items="mailings",
            on_click=open_mailing,  # type: ignore[arg-type]
            type_factory=int,
        ),
        id="mailings",
        hide_on_single_page=True,
        height=5,
        width=2,
        on_page_changed=sync_scroll("scroll_message_mailings"),
    ),
    BACK,
    getter=get_mailings_data,
    state=MailingsSG.items,
)
