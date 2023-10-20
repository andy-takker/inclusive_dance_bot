from aiogram import F, Router
from aiogram.filters import Command

from src.dialogs.admins import register_admin_dialogs
from src.dialogs.commands import start_command
from src.dialogs.users import register_user_dialogs
from src.ui_commands import Commands


def register_dialogs(router: Router) -> None:
    dialog_router = Router()

    # admin_router = register_admin_dialogs()
    # dialog_router.include_router(admin_router)

    user_router = register_user_dialogs()
    dialog_router.include_router(user_router)

    dialog_router.message(Command(Commands.START))(start_command)
    router.include_router(dialog_router)
