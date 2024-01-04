from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.messages import (
    CONFIRM_REGISTRATION_MESSAGE_TEMPLATE,
    THANK_FOR_REGISTRATION_MESSAGE,
)
from idb.bot.dialogs.users.states import MainMenuSG, RegistrationSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.db.uow import UnitOfWork
from idb.generals.enums import RegistrationField
from idb.logic.users import save_profile_user
from idb.utils.cache import AbstractBotCache


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
    await save_profile_user(
        uow=uow,
        user_id=c.from_user.id,
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
    dialog_manager: DialogManager, cache: AbstractBotCache, **kwargs: Any
) -> dict[str, Any]:
    user_types = filter(
        lambda ut: ut.id in dialog_manager.dialog_data[RegistrationField.USER_TYPE_IDS],
        (await cache.get_user_types()).values(),
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
