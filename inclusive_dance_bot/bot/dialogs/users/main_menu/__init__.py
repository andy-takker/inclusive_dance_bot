from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.users.main_menu import menu
from inclusive_dance_bot.bot.dialogs.users.states import MainMenuSG
from inclusive_dance_bot.bot.dialogs.utils.submenu_window import SubmenuWindow

dialog = Dialog(
    menu.window,
    SubmenuWindow(state=MainMenuSG.message),
)
