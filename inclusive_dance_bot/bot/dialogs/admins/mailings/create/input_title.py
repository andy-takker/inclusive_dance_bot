from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.admins.states import CreateMailingSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.bot.dialogs.utils.validators import validate_length

MESSAGE = "Введите тему сообщения.\n\nОграничение - 512 символов"


async def on_success(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["title"] = message.html_text
    await dialog_manager.next()


window = Window(
    Const(MESSAGE),
    TextInput(
        id="input_title",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_length(512),
    ),
    CANCEL,
    state=CreateMailingSG.title,
)
