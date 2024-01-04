from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.url.update import change_slug, change_value

dialog = Dialog(
    change_slug.window,
    change_value.window,
)
