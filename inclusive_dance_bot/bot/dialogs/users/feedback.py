from textwrap import dedent
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from inclusive_dance_bot.bot.dialogs.messages import ANSWER_ON_FEEDBACK_MESSAGE
from inclusive_dance_bot.bot.dialogs.users.states import FeedbackSG
from inclusive_dance_bot.bot.dialogs.users.windows.confirm import ConfirmWindow
from inclusive_dance_bot.bot.dialogs.utils.input_form_field import InputFormWindow
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.save_data import save_new_feedback

FEEDBACK_TITLE_FIELD = "title"
FEEDBACK_TEXT_FIELD = "text"
FEEDBACK_TYPE_FIELD = "type"

FEEDBACK_CONFIRM_TEMPLATE = dedent(
    """
Тема: <b>{title}</b>

Обращение:

{text}
"""
)


class FeedbackDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            InputFormWindow(
                state=FeedbackSG.input_title,
                message="Укажите тему обращения",
                field_name=FEEDBACK_TITLE_FIELD,
                is_first=True,
            ),
            InputFormWindow(
                state=FeedbackSG.input_message,
                message="Опишите Вашу проблему или предложение. "
                "Администраторы обязательно его расcмотрят",
                field_name=FEEDBACK_TEXT_FIELD,
            ),
            ConfirmWindow(
                state=FeedbackSG.confirm,
                on_click=on_click_confirm_feedback,
                confirm_button_text="Отправить",
                getter=get_confirm_data,
                format_template=FEEDBACK_CONFIRM_TEMPLATE,
            ),
            on_start=self.custom_on_start,
        )

    async def custom_on_start(
        self, data: dict[str, Any], dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data[FEEDBACK_TYPE_FIELD] = data["type"]


async def on_click_confirm_feedback(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await save_new_feedback(
        uow=uow,
        type=dialog_manager.dialog_data[FEEDBACK_TYPE_FIELD],
        user_id=c.from_user.id,
        title=dialog_manager.dialog_data[FEEDBACK_TITLE_FIELD],
        text=dialog_manager.dialog_data[FEEDBACK_TEXT_FIELD],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(  # type:ignore[union-attr]
        chat_id=c.from_user.id,
        text=ANSWER_ON_FEEDBACK_MESSAGE,
    )
    await dialog_manager.done()


async def get_confirm_data(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "title": dialog_manager.dialog_data[FEEDBACK_TITLE_FIELD],
        "text": dialog_manager.dialog_data[FEEDBACK_TEXT_FIELD],
    }
