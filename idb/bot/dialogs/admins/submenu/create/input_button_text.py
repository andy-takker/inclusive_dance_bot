from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateSubmenuSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.bot.dialogs.utils.validators import validate_length

MESSAGE = "Введите текст кнопки.\n\nОграничение - 64 символа"


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data["button_text"] = value
    await dialog_manager.next()


window = Window(
    Const(MESSAGE),
    TextInput(
        id="input_button_text",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_length(64),
    ),
    BACK,
    state=CreateSubmenuSG.button_text,
)
