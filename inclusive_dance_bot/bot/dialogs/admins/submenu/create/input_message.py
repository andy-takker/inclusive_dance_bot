from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.admins.states import CreateSubmenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK

TEMPLATE_MESSAGE = "Введите шаблон сообщения"


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data["message"] = value
    await dialog_manager.next()


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_message", on_success=on_success),  # type: ignore[arg-type]
    BACK,
    state=CreateSubmenuSG.message,
)
