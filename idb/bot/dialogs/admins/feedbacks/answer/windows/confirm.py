from datetime import UTC, datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import FeedbackAnswerSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork
from idb.logic.answer import create_feedback_answer
from idb.logic.feedback import update_answered_feedback


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    feedback_id = int(dialog_manager.start_data["feedback_id"])
    text = str(dialog_manager.current_context().widget_data["input_answer"])
    answer = await create_feedback_answer(
        uow=uow,
        feedback_id=feedback_id,
        text=text,
        from_user_id=dialog_manager.event.from_user.id,  # type: ignore[union-attr]
    )

    await c.bot.send_message(  # type: ignore[union-attr]
        chat_id=answer.to_user_id,
        text=answer.text,
    )
    await update_answered_feedback(
        uow=uow,
        feedback_id=feedback_id,
        dt=datetime.now(UTC),
    )
    await dialog_manager.done()


window = Window(
    Const("Отправить сообщение?"),
    Row(CANCEL, Button(text=Const("📨 Да"), id="send_message", on_click=on_click)),
    state=FeedbackAnswerSG.confirm,
)
