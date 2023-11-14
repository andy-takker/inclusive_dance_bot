from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.users.states import FeedbackSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.enums import FeedbackField


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data[FeedbackField.TEXT] = value
    await dialog_manager.next()


window = Window(
    Const(
        "Опишите Вашу проблему или предложение. Администраторы обязательно его рассмотрят"
    ),
    TextInput("input_message_id", on_success=on_success),  # type: ignore[arg-type]
    BACK,
    state=FeedbackSG.input_text,
)
