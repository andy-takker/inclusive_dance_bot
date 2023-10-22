from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.admins.windows.main_menu import MainMenuWindow
from inclusive_dance_bot.bot.states import MainMenuSG


class AdminMainMenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(MainMenuWindow(state=MainMenuSG.main_menu))
