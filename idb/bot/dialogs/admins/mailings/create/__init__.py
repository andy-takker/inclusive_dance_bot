from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.mailings.create import (
    choose_user_types,
    confirm,
    input_content,
    input_date,
    input_is_immediately,
    input_time,
    input_title,
)

dialog = Dialog(
    input_title.window,
    input_content.window,
    choose_user_types.window,
    input_is_immediately.window,
    input_date.window,
    input_time.window,
    confirm.window,
)
