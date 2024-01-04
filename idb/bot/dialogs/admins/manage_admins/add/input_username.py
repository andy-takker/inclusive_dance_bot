from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import AddAdminSG
from idb.bot.dialogs.messages import ADD_ADMIN_MESSAGE
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork
from idb.exceptions import UserNotFoundError
from idb.logic.users import add_user_to_admins


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.show_mode = ShowMode.SEND
    if message.entities is None or message.entities[0].type != "mention":
        await message.answer("Вы должны написать имя телеграм пользователя через @")
        return
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    username = message.entities[0].extract_from(value)[1:]
    try:
        await add_user_to_admins(uow=uow, username=username)
        await message.answer(f"Пользователь @{username} добавлен в администраторы")
        await dialog_manager.done()
    except UserNotFoundError:
        await message.answer(
            "Пользователь с таким ником не найден или он уже администратор. Проверьте!"
        )


window = Window(
    Const(ADD_ADMIN_MESSAGE),
    TextInput(id="input_username", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=AddAdminSG.input_username,
)
