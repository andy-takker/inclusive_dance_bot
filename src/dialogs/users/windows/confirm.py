from textwrap import dedent
from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.db.tmp import save_new_user
from src.db.uow.main import UnitOfWork
from src.dialogs.users.messages import THANK_FOR_REGISTRATION_MESSAGE
from src.states import MainMenuSG


class ConfirmWindow(Window):
    message_template = dedent(
        """
    Проверьте Ваши данные

    ФИО: {name}
    Регион: {region}
    Вы являетесь: {user_types}
    Телефон: {phone_number}
    """
    )

    def __init__(
        self,
        state: State,
    ):
        super().__init__(
            Format(text=self.message_template),
            Back(Const("Назад")),
            Button(Const("Сохранить"), id="confirm", on_click=on_click_save),
            state=state,
            getter=get_confirm_data,
        )


async def on_click_save(
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
        chat_id=c.from_user.id, text=THANK_FOR_REGISTRATION_MESSAGE
    )
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenuSG.main_menu)


async def get_confirm_data(
    dialog_manager: DialogManager, uow: UnitOfWork, **kwargs: Any
) -> dict[str, Any]:
    user_types = await uow.users.get_user_types_by_ids(
        ids=dialog_manager.dialog_data["user_type_ids"]
    )
    return {
        "name": dialog_manager.dialog_data["name"],
        "region": dialog_manager.dialog_data["region"],
        "user_types": ", ".join(map(lambda x: x.name, user_types)),
        "phone_number": dialog_manager.dialog_data["phone_number"],
    }
