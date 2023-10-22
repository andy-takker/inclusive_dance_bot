from textwrap import dedent
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from inclusive_dance_bot.bot.dialogs.messages import (
    INPUT_NAME_MESSAGE,
    INPUT_PHONE_NUMBER_MESSAGE,
    INPUT_REGION_MESSAGE,
    THANK_FOR_REGISTRATION_MESSAGE,
)
from inclusive_dance_bot.bot.dialogs.users.windows.choose_user_types import (
    ChooseUserTypesWindow,
)
from inclusive_dance_bot.bot.dialogs.users.windows.confirm import ConfirmWindow
from inclusive_dance_bot.bot.dialogs.utils.input_form_field import InputFormWindow
from inclusive_dance_bot.bot.states import MainMenuSG, RegistrationSG
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.save_data import save_new_user
from inclusive_dance_bot.services.storage import Storage

CONFIRM_REGISTRATION_MESSAGE_TEMPLATE = dedent(
    """
Проверьте Ваши данные

ФИО: {name}
Регион: {region}
Вы являетесь: {user_types}
Телефон: {phone_number}
"""
)


class RegistrationDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            InputFormWindow(
                state=RegistrationSG.input_name,
                field_name="name",
                message=INPUT_NAME_MESSAGE,
                is_first=True,
            ),
            ChooseUserTypesWindow(
                state=RegistrationSG.choose_types,
            ),
            InputFormWindow(
                state=RegistrationSG.input_place,
                field_name="region",
                message=INPUT_REGION_MESSAGE,
            ),
            InputFormWindow(
                state=RegistrationSG.input_phone_number,
                field_name="phone_number",
                message=INPUT_PHONE_NUMBER_MESSAGE,
            ),
            ConfirmWindow(
                state=RegistrationSG.confirm,
                format_template=CONFIRM_REGISTRATION_MESSAGE_TEMPLATE,
                on_click=on_click_confirm_registration,
                getter=get_confirm_registration_data,
            ),
        )


async def on_click_confirm_registration(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await save_new_user(
        uow=uow,
        user_id=c.from_user.id,
        name=dialog_manager.dialog_data["name"],
        region=dialog_manager.dialog_data["region"],
        phone_number=dialog_manager.dialog_data["phone_number"],
        user_type_ids=dialog_manager.dialog_data["user_type_ids"],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(  # type: ignore[union-attr]
        chat_id=c.from_user.id,
        text=THANK_FOR_REGISTRATION_MESSAGE,
    )
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenuSG.main_menu)


async def get_confirm_registration_data(
    dialog_manager: DialogManager, storage: Storage, **kwargs: Any
) -> dict[str, Any]:
    user_types = filter(
        lambda ut: ut.id in dialog_manager.dialog_data["user_type_ids"],
        (await storage.get_user_types()).values(),
    )
    return {
        "name": dialog_manager.dialog_data["name"],
        "region": dialog_manager.dialog_data["region"],
        "user_types": ", ".join(map(lambda x: x.name, user_types)),
        "phone_number": dialog_manager.dialog_data["phone_number"],
    }
