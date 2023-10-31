from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.users.states import MainMenuSG
from inclusive_dance_bot.bot.dialogs.users.windows.main_menu import MainMenuWindow
from inclusive_dance_bot.bot.dialogs.users.windows.submenu import SubmenuWindow


class MainMenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            MainMenuWindow(state=MainMenuSG.menu),
            SubmenuWindow(state=MainMenuSG.message),
        )
