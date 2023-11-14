from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.submenu.read import item, items

dialog = Dialog(
    items.window,
    item.window,
)
