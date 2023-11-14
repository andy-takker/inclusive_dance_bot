from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.messages import INPUT_PHONE_MESSAGE
from inclusive_dance_bot.bot.dialogs.users.states import RegistrationSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data["phone"] = value
    await dialog_manager.next()


window = Window(
    Const(INPUT_PHONE_MESSAGE),
    TextInput("input_phone_id", on_success=on_success),  # type: ignore[arg-type]
    BACK,
    state=RegistrationSG.input_phone,
)
