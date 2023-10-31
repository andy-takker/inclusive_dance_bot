from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.url.create import (
    confirm,
    input_slug,
    input_value,
)

dialog = Dialog(
    input_slug.window,
    input_value.window,
    confirm.window,
)
