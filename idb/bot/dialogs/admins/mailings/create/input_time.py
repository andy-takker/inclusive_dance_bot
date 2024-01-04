from datetime import time

from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateMailingSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.bot.dialogs.utils.validators import validate_time

MESSAGE = "Введите время отправки сообщения по Москве\n\nФормат: ЧЧ:ММ"


async def on_success(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: time,
) -> None:
    dialog_manager.dialog_data["time"] = value.isoformat(timespec="minutes")
    await dialog_manager.next()


window = Window(
    Const(MESSAGE),
    TextInput(
        id="input_time",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_time(),
    ),
    BACK,
    state=CreateMailingSG.time,
)
