from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminCreateSubmenuSG,
    AdminSubmenuSG,
)
from inclusive_dance_bot.services.storage import Storage

SCROLL_ID = "submenu_scroll_id"


async def get_submenu_list_data(storage: Storage, **kwargs: Any) -> dict[str, Any]:
    return {"submenus": (await storage.get_submenus()).values()}


async def open_submenu(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, submenu_id: int
) -> None:
    pass


window = Window(
    Const("Подменю"),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_submenu",
            item_id_getter=lambda x: str(x.id),
            items="submenus",
            on_click=open_submenu,  # type: ignore[arg-type]
            type_factory=int,
        ),
        id=SCROLL_ID,
        width=5,
        height=3,
    ),
    Start(
        text=Const("Добавить подменю"),
        id="create_submenu",
        state=AdminCreateSubmenuSG.input_message,
    ),
    Cancel(text=Const("Назад")),
    state=AdminSubmenuSG.items,
    getter=get_submenu_list_data,
)
