from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format, List

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminSubmenuSG,
    CreateSubmenuSG,
)
from inclusive_dance_bot.bot.dialogs.utils import sync_scroll
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.logic.storage import Storage

SCROLL_KBD_ID = "submenu_scroll_id"
SCROLL_MESSAGE_ID = "submenu_message_scroll_id"


async def get_submenu_list_data(storage: Storage, **kwargs: Any) -> dict[str, Any]:
    return {"submenus": list((await storage.get_submenus()).values())}


async def open_submenu(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, submenu_id: int
) -> None:
    dialog_manager.dialog_data["submenu_id"] = submenu_id
    await dialog_manager.next()


window = Window(
    Const("Подменю\n"),
    List(
        Format("[{pos}] {item.button_text} {item.id}\n{item.type}"),
        items="submenus",
        id=SCROLL_MESSAGE_ID,
        page_size=10,
        sep="\n\n",
    ),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_submenu",
            item_id_getter=lambda x: x.id,
            items="submenus",
            on_click=open_submenu,  # type: ignore[arg-type]
            type_factory=int,
        ),
        id=SCROLL_KBD_ID,
        width=5,
        height=2,
        on_page_changed=sync_scroll(SCROLL_MESSAGE_ID),
    ),
    Start(
        text=Const("Добавить подменю"),
        id="create_submenu",
        state=CreateSubmenuSG.type,
    ),
    CANCEL,
    state=AdminSubmenuSG.items,
    getter=get_submenu_list_data,
)
