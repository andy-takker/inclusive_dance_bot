from aiogram_dialog import Dialog

from inclusive_dance_bot.bot.dialogs.users.windows.entity import EntityWindow
from inclusive_dance_bot.bot.dialogs.users.windows.main_menu import MainMenuWindow
from inclusive_dance_bot.bot.states import MainMenuSG


class MainMenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            MainMenuWindow(state=MainMenuSG.main_menu),
            EntityWindow(state=MainMenuSG.message),
        )
