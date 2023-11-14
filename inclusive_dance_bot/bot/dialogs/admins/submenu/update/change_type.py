from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.admins.states import ChangeSubmenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import SubmenuType
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.submenu import update_submenu_by_id


async def get_submenu_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "submenu": await storage.get_submenu_by_id(
            dialog_manager.start_data["submenu_id"]
        ),
        "submenu_types": list(SubmenuType),
    }


async def on_click(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    type_: str,
) -> None:
    submenu_id = dialog_manager.start_data["submenu_id"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    storage: Storage = dialog_manager.middleware_data["storage"]
    await update_submenu_by_id(
        uow=uow,
        storage=storage,
        submenu_id=submenu_id,
        type_=SubmenuType(type_),
    )
    await dialog_manager.done()


TEMPLATE_MESSAGE = "Выберите новый тип подменю\n\nТекущее значение: {submenu.type}"

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
    state=ChangeSubmenuSG.type,
    getter=get_submenu_data,
)
