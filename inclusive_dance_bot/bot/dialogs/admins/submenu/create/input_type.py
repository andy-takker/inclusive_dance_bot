from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.admins.states import CreateSubmenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.enums import SubmenuType


async def get_submenu_data(**kwargs: Any) -> dict[str, Any]:
    return {
        "submenu_types": list(SubmenuType),
    }


async def on_click(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    type_: str,
) -> None:
    dialog_manager.dialog_data["type"] = type_
    await dialog_manager.next()


TEMPLATE_MESSAGE = "Выберите тип подменю"

window = Window(
    Format(TEMPLATE_MESSAGE),
    Column(
        Select(
            id="submenu_types",
            text=Format("{item}"),
            item_id_getter=lambda x: x,
            items="submenu_types",
            on_click=on_click,  # type: ignore[arg-type]
        ),
    ),
    CANCEL,
    state=CreateSubmenuSG.type,
    getter=get_submenu_data,
)
