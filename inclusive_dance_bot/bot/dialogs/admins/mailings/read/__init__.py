from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.mailings.read import item, items, menu

dialog = Dialog(
    menu.window,
    items.window,
    item.window,
)
