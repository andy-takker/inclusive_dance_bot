from aiogram_dialog import Dialog

from src.dialogs.users.windows.entity import EntityWindow
from src.dialogs.users.windows.main_menu import MainMenuWindow
from src.states import MainMenuSG


class MainMenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            MainMenuWindow(state=MainMenuSG.main_menu),
            EntityWindow(state=MainMenuSG.message),
        )
