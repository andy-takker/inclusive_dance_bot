from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.messages import INPUT_NAME_MESSAGE
from inclusive_dance_bot.bot.dialogs.users.states import RegistrationSG
from inclusive_dance_bot.enums import RegistrationField


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data[RegistrationField.NAME] = value
    await dialog_manager.next()


window = Window(
    Const(INPUT_NAME_MESSAGE),
    TextInput("input_name_id", on_success=on_success),  # type: ignore[arg-type]
    Cancel(text=Const("Отмена")),
    state=RegistrationSG.input_name,
)
