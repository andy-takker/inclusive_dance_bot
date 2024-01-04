from aiogram_dialog import Dialog

from idb.bot.dialogs.users.registration import (
    choose_user_types,
    confirm,
    input_name,
    input_phone,
    input_region,
)

dialog = Dialog(
    input_name.window,
    choose_user_types.window,
    input_region.window,
    input_phone.window,
    confirm.window,
)
