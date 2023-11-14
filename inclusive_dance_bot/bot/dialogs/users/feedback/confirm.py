from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.messages import (
    ANSWER_ON_FEEDBACK_MESSAGE,
    FEEDBACK_CONFIRM_TEMPLATE,
)
from inclusive_dance_bot.bot.dialogs.users.states import FeedbackSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import FeedbackField
from inclusive_dance_bot.logic.feedback import create_feedback


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await create_feedback(
        uow=uow,
        type=dialog_manager.dialog_data[FeedbackField.TYPE],
        user_id=c.from_user.id,
        title=dialog_manager.dialog_data[FeedbackField.TITLE],
        text=dialog_manager.dialog_data[FeedbackField.TEXT],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(  # type:ignore[union-attr]
        chat_id=c.from_user.id,
        text=ANSWER_ON_FEEDBACK_MESSAGE,
    )
    await dialog_manager.done()


async def get_feedback_data(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        FeedbackField.TITLE: dialog_manager.dialog_data[FeedbackField.TITLE],
        FeedbackField.TEXT: dialog_manager.dialog_data[FeedbackField.TEXT],
    }


window = Window(
    Format(FEEDBACK_CONFIRM_TEMPLATE),
    Row(
        BACK,
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=FeedbackSG.confirm,
    getter=get_feedback_data,
)
