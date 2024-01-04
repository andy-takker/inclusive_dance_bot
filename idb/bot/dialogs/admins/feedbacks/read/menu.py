from typing import Any

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import FeedbackItemsSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork


async def get_data(uow: UnitOfWork, **kwargs: Any) -> dict[str, Any]:
    archive_feedback_count = await uow.feedbacks.archive_count()
    new_feedback_count = await uow.feedbacks.new_count()
    return {
        "archive_feedback_count": archive_feedback_count,
        "new_feedback_count": new_feedback_count,
    }


window = Window(
    Const("Обратная связь"),
    SwitchTo(
        text=Format("🆕 Новые сообщения ({new_feedback_count})"),
        state=FeedbackItemsSG.new,
        id="new_feedbacks",
    ),
    SwitchTo(
        text=Format("👁 Просмотренные сообщения ({archive_feedback_count})"),
        state=FeedbackItemsSG.archived,
        id="archive_feedbacks",
    ),
    CANCEL,
    state=FeedbackItemsSG.menu,
    getter=get_data,
)
