from datetime import date

from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateMailingSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.bot.dialogs.utils.validators import validate_date

MESSAGE = "Введите дату отправки сообщения\n\nФормат: ДД.ММ.ГГГГ"


async def on_success(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: date,
) -> None:
    dialog_manager.dialog_data["date"] = value.isoformat()
    await dialog_manager.next()


window = Window(
    Const(MESSAGE),
    TextInput(
        id="input_date",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_date(),
    ),
    BACK,
    state=CreateMailingSG.date,
)
