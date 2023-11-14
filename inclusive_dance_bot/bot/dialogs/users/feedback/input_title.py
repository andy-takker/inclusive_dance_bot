from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.users.states import FeedbackSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.enums import FeedbackField


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data[FeedbackField.TITLE] = value
    await dialog_manager.next()


window = Window(
    Const("Введите тему обращения"),
    TextInput("input_title_id", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=FeedbackSG.input_title,
)
