from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.messages import (
    CONFIRM_REGISTRATION_MESSAGE_TEMPLATE,
    THANK_FOR_REGISTRATION_MESSAGE,
)
from inclusive_dance_bot.bot.dialogs.users.states import MainMenuSG, RegistrationSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import RegistrationField
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.user import create_user


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    dialog_manager.show_mode = ShowMode.SEND
    username = c.from_user.username
    if username is None:
        await c.bot.send_message(  # type: ignore[union-attr]
            chat_id=c.from_user.id,
            text="У Вас нет username, пожалуйста, придумайте его прежде чем "
            " регистрироваться в боте",
        )
        return
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await create_user(
        uow=uow,
        user_id=c.from_user.id,
        username=username,
        name=dialog_manager.dialog_data[RegistrationField.NAME],
        region=dialog_manager.dialog_data[RegistrationField.REGION],
        phone_number=dialog_manager.dialog_data[RegistrationField.PHONE],
        user_type_ids=dialog_manager.dialog_data[RegistrationField.USER_TYPE_IDS],
    )
    await c.bot.send_message(  # type: ignore[union-attr]
        chat_id=c.from_user.id,
        text=THANK_FOR_REGISTRATION_MESSAGE,
    )
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenuSG.menu)


async def get_user_data(
    dialog_manager: DialogManager, storage: Storage, **kwargs: Any
) -> dict[str, Any]:
    user_types = filter(
        lambda ut: ut.id in dialog_manager.dialog_data[RegistrationField.USER_TYPE_IDS],
        (await storage.get_user_types()).values(),
    )
    return {
        "name": dialog_manager.dialog_data[RegistrationField.NAME],
        "region": dialog_manager.dialog_data[RegistrationField.REGION],
        "user_types": ", ".join(map(lambda x: x.name, user_types)),
        "phone": dialog_manager.dialog_data[RegistrationField.PHONE],
    }


window = Window(
    Format(CONFIRM_REGISTRATION_MESSAGE_TEMPLATE),
    Row(
        BACK,
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=RegistrationSG.confirm,
    getter=get_user_data,
)
