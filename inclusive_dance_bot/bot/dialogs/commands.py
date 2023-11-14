from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from inclusive_dance_bot.bot.dialogs.admins.states import AdminMainMenuSG
from inclusive_dance_bot.bot.dialogs.messages import START_MESSAGE
from inclusive_dance_bot.bot.dialogs.users.states import MainMenuSG as UserMainMenuSG
from inclusive_dance_bot.bot.dialogs.users.states import RegistrationSG
from inclusive_dance_bot.logic.user import MegaUser


async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    user: MegaUser,
) -> None:
    if user.is_admin:
        await dialog_manager.start(AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)
    elif user.is_anonymous:
        await message.answer(START_MESSAGE)
        await dialog_manager.start(
            RegistrationSG.input_name,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(UserMainMenuSG.menu, mode=StartMode.RESET_STACK)
