from aiogram.fsm.state import State, StatesGroup


class RegistrationSG(StatesGroup):
    input_name = State()
    choose_types = State()
    input_region = State()
    input_phone = State()
    confirm = State()


class MainMenuSG(StatesGroup):
    menu = State()
    message = State()


class SubmenuSG(StatesGroup):
    list_ = State()
    submenu = State()


class FeedbackSG(StatesGroup):
    input_title = State()
    input_text = State()
    confirm = State()
