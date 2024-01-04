from aiogram.fsm.state import State, StatesGroup


class AdminMainMenuSG(StatesGroup):
    menu = State()


class AdminFeedbackSG(StatesGroup):
    items = State()


class AdminSubmenuSG(StatesGroup):
    items = State()
    info = State()


class CreateSubmenuSG(StatesGroup):
    type = State()
    weight = State()
    message = State()
    button_text = State()
    confirm = State()


class ChangeSubmenuSG(StatesGroup):
    type = State()
    weight = State()
    button_text = State()
    message = State()


class DeleteSubmenuSG(StatesGroup):
    confirm = State()


class ReadUrlSG(StatesGroup):
    items = State()
    item = State()


class CreateUrlSG(StatesGroup):
    slug = State()
    value = State()
    confirm = State()


class ChangeUrlSG(StatesGroup):
    slug = State()
    value = State()


class DeleteUrlSG(StatesGroup):
    confirm = State()


class ManageAdminSG(StatesGroup):
    items = State()


class AddAdminSG(StatesGroup):
    input_username = State()


class DeleteAdminSG(StatesGroup):
    confirm = State()


class MailingsSG(StatesGroup):
    menu = State()
    items = State()
    item = State()


class CancelMailingSG(StatesGroup):
    confirm = State()


class FeedbackAnswerSG(StatesGroup):
    input_message = State()
    confirm = State()


class FeedbackItemsSG(StatesGroup):
    menu = State()
    new = State()
    archived = State()
    item = State()


class CreateMailingSG(StatesGroup):
    title = State()
    content = State()
    user_types = State()
    is_immediately = State()
    date = State()
    time = State()
    confirm = State()
