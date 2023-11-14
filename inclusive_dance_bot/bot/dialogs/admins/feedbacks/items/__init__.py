from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.feedbacks.items import archive, new

dialog = Dialog(
    new.window,
    archive.window,
)
