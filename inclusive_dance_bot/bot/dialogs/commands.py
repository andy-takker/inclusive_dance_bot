from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from inclusive_dance_bot.bot.dialogs.messages import START_MESSAGE
from inclusive_dance_bot.bot.states import MainMenuSG, RegistrationSG
from inclusive_dance_bot.db.uow.main import UnitOfWork


async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    uow: UnitOfWork,
) -> None:
    if message.from_user is None:
        return
    user = await uow.users.get_by_id_or_none(message.from_user.id)
    if user is not None:
        await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
    else:
        await message.answer(START_MESSAGE)
        await dialog_manager.start(
            RegistrationSG.input_name,
            mode=StartMode.RESET_STACK,
        )
