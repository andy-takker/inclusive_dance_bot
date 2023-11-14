from typing import Any

from aiogram_dialog import Dialog, DialogManager

from inclusive_dance_bot.bot.dialogs.users.feedback import (
    confirm,
    input_text,
    input_title,
)
from inclusive_dance_bot.enums import FeedbackField


async def on_start(data: dict[str, Any], dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data[FeedbackField.TYPE] = data[FeedbackField.TYPE]


dialog = Dialog(
    input_title.window,
    input_text.window,
    confirm.window,
    on_start=on_start,
)
