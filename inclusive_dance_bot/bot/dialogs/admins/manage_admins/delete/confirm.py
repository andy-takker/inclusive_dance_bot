from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import DeleteAdminSG
from inclusive_dance_bot.bot.dialogs.users.states import MainMenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.user import delete_from_admins


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.start_data["user_id"]
    await delete_from_admins(uow=uow, user_id=user_id)
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(  # type: ignore[union-attr]
        c.from_user.id, text="Пользователь был лишен прав администратора"
    )
    await dialog_manager.bg(chat_id=user_id).start(
        state=MainMenuSG.menu, mode=StartMode.RESET_STACK
    )
    await dialog_manager.done()


async def get_user(
    uow: UnitOfWork, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    user_id = dialog_manager.start_data["user_id"]
    return {"user": await uow.users.get_by_id(user_id=user_id)}


window = Window(
    Format("Вы действительно хотите лишить @{user.username} прав администратора?"),
    Row(
        CANCEL,
        Button(text=Const("Подтвердить"), id="delete_from_admins", on_click=on_click),
    ),
    state=DeleteAdminSG.confirm,
    getter=get_user,
)
