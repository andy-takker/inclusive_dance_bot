from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    DeleteSubmenuSG,
)
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.bot.dialogs.utils.getters import get_submenu_data
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.submenu import delete_submenu_by_id


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    submenu_id = dialog_manager.start_data["submenu_id"]
    await delete_submenu_by_id(uow=uow, storage=storage, submenu_id=submenu_id)
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
