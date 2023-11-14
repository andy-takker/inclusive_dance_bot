from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.manage_admins.add import input_username

dialog = Dialog(
    input_username.window,
)
