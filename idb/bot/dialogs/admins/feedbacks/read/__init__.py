from aiogram_dialog import Dialog

from idb.bot.dialogs.admins.feedbacks.read import (
    item,
    menu,
    new,
    viewed,
)

dialog = Dialog(
    menu.window,
    new.window,
    viewed.window,
    item.window,
)
