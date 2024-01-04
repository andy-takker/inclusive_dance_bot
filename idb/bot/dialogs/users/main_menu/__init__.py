from aiogram_dialog import Dialog

from idb.bot.dialogs.users.main_menu import menu
from idb.bot.dialogs.users.states import MainMenuSG
from idb.bot.dialogs.utils.submenu_window import SubmenuWindow

dialog = Dialog(
    menu.window,
    SubmenuWindow(state=MainMenuSG.message),
)
