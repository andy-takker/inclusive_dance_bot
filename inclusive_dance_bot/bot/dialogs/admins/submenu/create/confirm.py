from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    CreateSubmenuSG,
)
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.submenu import create_submenu


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await create_submenu(
        uow=uow,
        storage=storage,
        type=dialog_manager.dialog_data["type"],
        weight=dialog_manager.dialog_data["weight"],
        message=dialog_manager.dialog_data["message"],
        button_text=dialog_manager.dialog_data["button_text"],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Подменю было сохранено")  # type: ignore[union-attr]
    await dialog_manager.start(state=AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)


window = Window(
    Format(
        "Сохранить подменю?\n\n"
        "Тип: {dialog_data[type]}\nВес: {dialog_data[weight]}\n"
        "Текст кнопки: {dialog_data[button_text]}\nСообщение:\n{dialog_data[message]}"
    ),
    Row(
        BACK,
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=CreateSubmenuSG.confirm,
)
