from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from idb.bot.dialogs.admins.states import (
    FeedbackAnswerSG,
    FeedbackItemsSG,
)
from idb.bot.dialogs.utils.start_with_data import start_with_data
from idb.db.uow import UnitOfWork
from idb.generals.enums import FEEDBACK_TYPE_MAPPING, FeedbackStatus

FEEDBACK_TEMPLATE = """
Тема: <b>{{ feedback.title }}</b>
Тип: <i>{{ feedback_type }}</i>
Отправлено: <i>{{ feedback.created_at|as_local_fmt }}</i>
Просмотрено: <i>{{ feedback.viewed_at|as_local_fmt }}</i>

{{ feedback.text }}

{% if answers %}

<b>Ответы:</b>

{% for answer in answers %}
Отправлено: {{ answer.created_at|as_local_fmt }}
<i>{{ answer.text }}</i>
=======

{% endfor %}

{% endif %}
"""


async def get_feedback_data(
    uow: UnitOfWork, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    feedback_id = dialog_manager.dialog_data["feedback_id"]
    feedback = await uow.feedbacks.read_by_id(feedback_id)
    return {
        "feedback": feedback,
        "answers": await uow.answer.history(feedback_id=feedback_id),
        "feedback_type": FEEDBACK_TYPE_MAPPING[feedback.type],
    }


async def back(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    if dialog_manager.dialog_data["back"] == FeedbackStatus.NEW:
        await dialog_manager.switch_to(FeedbackItemsSG.new)
    elif dialog_manager.dialog_data["back"] == FeedbackStatus.ARCHIVED:
        await dialog_manager.switch_to(FeedbackItemsSG.archived)


def _when(data: dict, widget: Button, dialog_manager: DialogManager) -> bool:
    feedback = data.get("feedback")
    if feedback is None:
        return False
    return feedback.is_answered


window = Window(
    Const("Обратная связь"),
    Jinja(FEEDBACK_TEMPLATE),
    Button(
        Const("✏️ Написать пользователю"),
        id="start_answer",
        on_click=start_with_data(
            state=FeedbackAnswerSG.input_message,
            field="feedback_id",
        ),
    ),
    Button(Const("⬅️ Назад"), id="back", on_click=back),
    state=FeedbackItemsSG.item,
    getter=get_feedback_data,
)
