from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.admins.states import AdminSubmenuSG

window = Window(
    Const("Подменю"),
    Back(Const("Назад")),
    state=AdminSubmenuSG.info,
)
