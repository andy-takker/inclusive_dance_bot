from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.submenu.create import (
    confirm,
    input_button_text,
    input_message,
    input_type,
    input_weight,
)

dialog = Dialog(
    input_type.window,
    input_weight.window,
    input_button_text.window,
    input_message.window,
    confirm.window,
)
