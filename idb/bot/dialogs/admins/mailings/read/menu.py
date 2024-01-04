from collections.abc import Callable
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Next, Start
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateMailingSG, MailingsSG
from idb.bot.dialogs.utils.buttons import CANCEL


def next_with_data(data: dict[str, Any]) -> Callable:
    async def on_click(
        c: CallbackQuery, button: Button, dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data.update(data)

    return on_click


window = Window(
    Const("Рассылки"),
    Start(
        text=Const("Создать рассылку"), state=CreateMailingSG.title, id="create_mailing"
    ),
    Next(
        text=Const("Запланированные рассылки"),
        on_click=next_with_data({"is_sent": False}),
        id="new_mailing_items",
    ),
    Next(
        text=Const("Архив"),
        on_click=next_with_data({"is_sent": True}),
        id="archive_mailing_items",
    ),
    CANCEL,
    state=MailingsSG.menu,
)
