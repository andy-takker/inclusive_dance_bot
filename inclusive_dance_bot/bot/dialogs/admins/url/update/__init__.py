from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.url.update import change_slug, change_value

dialog = Dialog(
    change_slug.window,
    change_value.window,
)
