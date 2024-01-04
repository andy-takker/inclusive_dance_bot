from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.mailings.read import item, items, menu

dialog = Dialog(
    menu.window,
    items.window,
    item.window,
)
