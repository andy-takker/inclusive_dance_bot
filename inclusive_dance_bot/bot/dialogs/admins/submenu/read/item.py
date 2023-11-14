from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminSubmenuSG,
    ChangeSubmenuSG,
    DeleteSubmenuSG,
)
from inclusive_dance_bot.bot.dialogs.messages import SUBMENU_TEMPLATE
from inclusive_dance_bot.bot.dialogs.utils import start_with_data
from inclusive_dance_bot.logic.storage import Storage

SUBMENU_ID = "submenu_id"


async def get_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    s = await storage.get_submenu_by_id(dialog_manager.dialog_data[SUBMENU_ID])
    return {"submenu": s}


window = Window(
    Format(SUBMENU_TEMPLATE),
    Button(
        Const("Изменить тип"),
        id="change_submenu_type",
        on_click=start_with_data(state=ChangeSubmenuSG.type, field=SUBMENU_ID),
    ),
    Button(
        Const("Изменить вес"),
        id="change_submenu_weight",
        on_click=start_with_data(state=ChangeSubmenuSG.weight, field=SUBMENU_ID),
    ),
    Button(
        Const("Изменить текст кнопки"),
        id="change_submenu_button_text",
        on_click=start_with_data(state=ChangeSubmenuSG.button_text, field=SUBMENU_ID),
    ),
    Button(
        Const("Изменить значение"),
        id="change_submenu_message",
        on_click=start_with_data(state=ChangeSubmenuSG.message, field=SUBMENU_ID),
    ),
    Button(
        Const("Удалить подменю"),
        id="delete_submenu",
        on_click=start_with_data(state=DeleteSubmenuSG.confirm, field=SUBMENU_ID),
    ),
    Back(Const("Назад")),
    state=AdminSubmenuSG.info,
    getter=get_data,
)
