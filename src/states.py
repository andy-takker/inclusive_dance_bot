from aiogram.fsm.state import State, StatesGroup


class RegistrationSG(StatesGroup):
    input_name = State()
    choose_types = State()
    input_place = State()
    input_phone_number = State()
    confirm = State()


class MainMenuSG(StatesGroup):
    main_menu = State()
    message = State()


class EntitySG(StatesGroup):
    list_ = State()
    entity = State()


class FeedbackSG(StatesGroup):
    input_title = State()
    input_message = State()
    confirm = State()
