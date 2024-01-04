from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja, List

from idb.bot.dialogs.admins.states import FeedbackItemsSG
from idb.bot.dialogs.utils.sync_scroll import sync_scroll
from idb.db.uow import UnitOfWork
from idb.generals.enums import FeedbackStatus

SCROLL_KBD_ID = "feedback_scroll_id"
SCROLL_MESSAGE_ID = "feedback_message_scroll_id"


async def get_feedbacks_list_data(uow: UnitOfWork, **kwargs: Any) -> dict[str, Any]:
    return {"feedbacks": await uow.feedbacks.viewed_items()}


async def open_feedback(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    feedback_id: int,
) -> None:
    dialog_manager.dialog_data["feedback_id"] = feedback_id
    dialog_manager.dialog_data["back"] = FeedbackStatus.ARCHIVED
    await dialog_manager.switch_to(FeedbackItemsSG.item)


HEAD_MESSAGE = """
Просмотренные сообщения
❌ - не ответили
✅ - ответили
"""

window = Window(
    Const(HEAD_MESSAGE),
    List(
        Jinja(
            "[{{ pos }}] {{ item.created_at|as_local_fmt }} {{ item.title }} "
            "{% if item.is_answered %}✅{% else %}❌{% endif %}"
        ),
        items="feedbacks",
        id=SCROLL_MESSAGE_ID,
        page_size=10,
    ),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_feedback",
            item_id_getter=lambda x: x.id,
            items="feedbacks",
            on_click=open_feedback,  # type: ignore[arg-type]
            type_factory=int,
        ),
        id=SCROLL_KBD_ID,
        width=5,
        height=2,
        hide_on_single_page=True,
        on_page_changed=sync_scroll(SCROLL_MESSAGE_ID),
    ),
    SwitchTo(Const("⬅️ Назад"), id="back", state=FeedbackItemsSG.menu),
    state=FeedbackItemsSG.archived,
    getter=get_feedbacks_list_data,
)
