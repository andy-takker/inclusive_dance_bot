from aiogram import Router

from src.dialogs.users.entity import EntityDialog
from src.dialogs.users.main_menu import MainMenuDialog
from src.dialogs.users.registration import RegistrationDialog


def register_user_dialogs() -> Router:
    dialog_router = Router(name="user_router")

    dialog_router.include_router(RegistrationDialog())
    dialog_router.include_router(MainMenuDialog())
    dialog_router.include_router(EntityDialog())

    return dialog_router
