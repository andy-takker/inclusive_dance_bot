from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.admins.states import CreateUrlSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data["value"] = value
    await dialog_manager.next()
    return


window = Window(
    Const("Введите значение для новой ссылки"),
    TextInput(id="input_value", on_success=on_success),  # type: ignore[arg-type]
    BACK,
    state=CreateUrlSG.value,
)
