from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.submenu.update import (
    change_button_text,
    change_message,
    change_type,
    change_weight,
)

dialog = Dialog(
    change_type.window,
    change_weight.window,
    change_button_text.window,
    change_message.window,
)
