from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const


class MainMenuWindow(Window):
    def __init__(self, state: State):
        super().__init__(Const("Меню администратора"), state=state)
