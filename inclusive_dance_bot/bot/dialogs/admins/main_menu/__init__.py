from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.main_menu.read import menu
from inclusive_dance_bot.bot.dialogs.admins.states import AdminMainMenuSG

dialog = Dialog(menu.window)
