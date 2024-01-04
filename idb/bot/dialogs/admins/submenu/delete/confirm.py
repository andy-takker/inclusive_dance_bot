from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    DeleteSubmenuSG,
)
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_submenu_data
from idb.db.uow import UnitOfWork
from idb.logic.submenu import delete_submenu_by_id
from idb.utils.cache import AbstractBotCache


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    submenu_id = dialog_manager.start_data["submenu_id"]
    await delete_submenu_by_id(uow=uow, cache=cache, submenu_id=submenu_id)
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Подменю было удалено")  # type: ignore[union-attr]
    await dialog_manager.start(state=AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)


window = Window(
    Format("Вы действительно хотите удалить подменю `{submenu.button_text}`"),
    Row(
        CANCEL,
        Button(text=Const("Удалить"), id="delete_submenu", on_click=on_click),
    ),
    state=DeleteSubmenuSG.confirm,
    getter=get_submenu_data,
)
