from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.messages import INPUT_NAME_MESSAGE
from idb.bot.dialogs.users.states import RegistrationSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.generals.enums import RegistrationField


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data[RegistrationField.NAME] = value
    await dialog_manager.next()


window = Window(
    Const(INPUT_NAME_MESSAGE),
    TextInput("input_name_id", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=RegistrationSG.input_name,
)
