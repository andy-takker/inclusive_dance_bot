from aiogram import Router
from aiogram.filters import Command

from inclusive_dance_bot.bot.dialogs import admins, users
from inclusive_dance_bot.bot.dialogs.commands import start_command
from inclusive_dance_bot.bot.ui_commands import Commands


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.include_routers(admins.dialog_router, users.dialog_router)
    dialog_router.message(Command(Commands.START))(start_command)
    router.include_router(dialog_router)
