from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format, Jinja

from idb.bot.dialogs.admins.states import (
    AdminSubmenuSG,
    ChangeSubmenuSG,
    DeleteSubmenuSG,
)
from idb.bot.dialogs.utils import start_with_data
from idb.bot.dialogs.utils.buttons import BACK
from idb.utils.cache import AbstractBotCache

SUBMENU_ID = "submenu_id"

SUBMENU_TEMPLATE = """\
<b>Подменю</b> {submenu.id}

<b>Тип:</b> {submenu.type}
<b>Текст кнопки:</b> {submenu.button_text}
<b>Вес:</b> {submenu.weight}
"""
SUBMENU_JINJA = """\
<b>Значение:</b>

{{ submenu.message }}
"""


async def get_data(
    cache: AbstractBotCache, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    s = await cache.get_submenu_by_id(dialog_manager.dialog_data[SUBMENU_ID])
    return {"submenu": s}


window = Window(
    Format(SUBMENU_TEMPLATE),
    Jinja(SUBMENU_JINJA),
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
    BACK,
    state=AdminSubmenuSG.info,
    getter=get_data,
)
