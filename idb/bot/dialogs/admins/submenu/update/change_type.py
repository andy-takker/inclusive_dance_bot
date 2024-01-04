from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from idb.bot.dialogs.admins.states import ChangeSubmenuSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork
from idb.generals.enums import SubmenuType
from idb.logic.submenu import update_submenu_by_id
from idb.utils.cache import AbstractBotCache


async def get_submenu_data(
    cache: AbstractBotCache, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "submenu": await cache.get_submenu_by_id(
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
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    await update_submenu_by_id(
        uow=uow,
        cache=cache,
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
