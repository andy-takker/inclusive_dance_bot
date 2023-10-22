from aiogram import Router

from inclusive_dance_bot.bot.dialogs.users.entity import EntityDialog
from inclusive_dance_bot.bot.dialogs.users.feedback import FeedbackDialog
from inclusive_dance_bot.bot.dialogs.users.main_menu import MainMenuDialog
from inclusive_dance_bot.bot.dialogs.users.registration import RegistrationDialog


def register_user_dialogs() -> Router:
    dialog_router = Router(name="user_router")

    dialog_router.include_router(RegistrationDialog())
    dialog_router.include_router(MainMenuDialog())
    dialog_router.include_router(EntityDialog())
    dialog_router.include_router(FeedbackDialog())

    return dialog_router
