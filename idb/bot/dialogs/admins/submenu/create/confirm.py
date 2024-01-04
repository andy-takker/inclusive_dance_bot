from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    CreateSubmenuSG,
)
from idb.bot.dialogs.utils.buttons import BACK
from idb.db.uow import UnitOfWork
from idb.logic.submenu import create_submenu
from idb.utils.cache import AbstractBotCache


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await create_submenu(
        uow=uow,
        cache=cache,
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
