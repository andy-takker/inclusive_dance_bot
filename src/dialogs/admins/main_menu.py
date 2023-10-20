from aiogram_dialog import Dialog

from src.dialogs.admins.windows.main_menu import MainMenuWindow
from src.states import MainMenuSG


class AdminMainMenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(MainMenuWindow(state=MainMenuSG.main_menu))
