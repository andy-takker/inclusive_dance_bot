from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateMailingSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.bot.dialogs.utils.validators import validate_length

MESSAGE = "Введите сообщение\n\nОграничение - 3072 символов"


async def on_success(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["content"] = message.html_text
    await dialog_manager.next()


window = Window(
    Const(MESSAGE),
    TextInput(
        id="input_content",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_length(3072),
    ),
    BACK,
    state=CreateMailingSG.content,
)
