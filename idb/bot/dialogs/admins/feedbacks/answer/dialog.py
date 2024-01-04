from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.feedbacks.answer.windows.confirm import (
    window as confirm_window,
)
from idb.bot.dialogs.admins.feedbacks.answer.windows.input_message import (
    window as input_message_window,
)

dialog = Dialog(
    input_message_window,
    confirm_window,
)
