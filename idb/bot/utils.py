from datetime import datetime

import pytz
from aiogram_dialog import DialogManager, ShowMode, StartMode

from idb.bot.dialogs.admins.states import AdminMainMenuSG
from idb.bot.dialogs.messages import START_MESSAGE
from idb.bot.dialogs.users.states import MainMenuSG, RegistrationSG
from idb.generals.models.user import BotUser

LOCAL_TZ = pytz.timezone("Europe/Moscow")


async def start_new_dialog(dialog_manager: DialogManager) -> None:
    user: BotUser = dialog_manager.middleware_data["user"]
    if user.is_admin:
        await dialog_manager.start(
            AdminMainMenuSG.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
        )
    elif user.is_anonymous:
        chat_id = dialog_manager.event.from_user.id  # type: ignore[union-attr]
        await dialog_manager.event.bot.send_message(  # type: ignore[union-attr]
            chat_id=chat_id,
            text=START_MESSAGE,
        )
        await dialog_manager.start(
            RegistrationSG.input_name,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(
            MainMenuSG.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
        )


def as_local_dt(dt: datetime) -> datetime:
    return dt.astimezone(LOCAL_TZ)


def as_local_fmt(dt: datetime) -> str:
    return as_local_dt(dt).strftime("%H:%M:%S %d.%m.%Y")
