from aiogram import Router
from aiogram.filters import Command

from idb.bot.dialogs.admins.router import (
    dialog_router as admin_dialog_router,
)
from idb.bot.dialogs.commands import start_command
from idb.bot.dialogs.users.router import (
    dialog_router as user_dialog_router,
)
from idb.bot.ui_commands import Commands


def register_dialogs(root_router: Router) -> None:
    dialog_router = Router()
    dialog_router.include_routers(admin_dialog_router, user_dialog_router)
    dialog_router.message(Command(Commands.START))(start_command)
    root_router.include_router(dialog_router)
