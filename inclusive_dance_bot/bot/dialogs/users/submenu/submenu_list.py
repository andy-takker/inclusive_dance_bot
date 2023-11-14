from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.users.states import SubmenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.logic.storage import Storage


async def get_submenu_data(
    dialog_manager: DialogManager, storage: Storage, **kwargs: Any
) -> dict[str, Any]:
    submenu_type = dialog_manager.dialog_data["type"]
    submenus = await storage.get_submenus()
    return {
        "submenus": list(filter(lambda x: x.type == submenu_type, submenus.values())),
        "message": dialog_manager.dialog_data["message"],
    }


async def open_message(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    submenu_id: int,
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    submenus = await storage.get_submenus()
    submenu = submenus[submenu_id]
    scrolling_text = dialog_manager.find("scroll_text")
    scrolling_text.widget.text = Format(submenu.message)  # type: ignore[union-attr]
    await dialog_manager.next()


window = Window(
    Format("{message}"),
    Column(
        Select(
            text=Format("{item.button_text}"),
            id="s_submenus",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            items="submenus",
            on_click=open_message,  # type: ignore[arg-type]
        ),
    ),
    CANCEL,
    state=SubmenuSG.list_,
    getter=get_submenu_data,
)
