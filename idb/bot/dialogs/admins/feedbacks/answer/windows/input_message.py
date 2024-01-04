from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import FeedbackAnswerSG
from idb.bot.dialogs.utils.buttons import CANCEL


async def on_success_next(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    await dialog_manager.next()


window = Window(
    Const("Введите сообщение"),
    TextInput(
        id="input_answer",
        on_success=on_success_next,  # type: ignore[arg-type]
    ),
    CANCEL,
    state=FeedbackAnswerSG.input_message,
)
