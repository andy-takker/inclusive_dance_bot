from aiogram.fsm.state import State, StatesGroup


class AdminMainMenuSG(StatesGroup):
    menu = State()


class AdminFeedbackSG(StatesGroup):
    items = State()


class AdminSubmenuSG(StatesGroup):
    items = State()
    info = State()


class AdminCreateSubmenuSG(StatesGroup):
    input_message = State()
    input_text = State()


class ReadUrlSG(StatesGroup):
    items = State()
    item = State()


class CreateUrlSG(StatesGroup):
    input_slug = State()
    input_value = State()
    confirm = State()


class ChangeUrlSG(StatesGroup):
    change_slug = State()
    change_value = State()


class DeleteUrlSG(StatesGroup):
    confirm = State()


class AdminManageAdminSG(StatesGroup):
    items = State()


class AdminSendMessageSG(StatesGroup):
    choose_user_types = State()
    input_message = State()
    input_media = State()
    input_datetime = State()
    confirm = State()
