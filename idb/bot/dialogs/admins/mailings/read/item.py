from datetime import timedelta
from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import CancelMailingSG, MailingsSG
from idb.bot.dialogs.utils import start_with_data
from idb.bot.dialogs.utils.buttons import BACK
from idb.db.uow import UnitOfWork
from idb.generals.enums import MailingStatus

TEMPLATE_MESSAGE = """
Рассылка

Тема: <b>{title}</b>
Создано: <i>{created_at}</i>
Отправка в: <i>{scheduled_at}</i>
Статус: <b>{status}</b>
Аудитория: <i>{user_types}</i>

{content}
"""


async def get_mailing(
    uow: UnitOfWork, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    mailing_id = dialog_manager.dialog_data["mailing_id"]
    mailing = await uow.mailings.get_by_id(mailing_id=mailing_id)

    scheduled_at = "Отправлено сразу"
    if mailing.scheduled_at:
        scheduled_at = (mailing.scheduled_at + timedelta(hours=3)).strftime(
            "%H:%M:%S %d.%m.%Y"
        )

    created_at = (mailing.created_at + timedelta(hours=3)).strftime("%H:%M:%S %d.%m.%Y")
    return {
        "title": mailing.title,
        "content": mailing.content,
        "scheduled_at": scheduled_at,
        "status": mailing.status,
        "created_at": created_at,
        "user_types": ", ".join(ut.name for ut in mailing.user_types),
    }


def when_(data: dict, widget: Button, dialog_manager: DialogManager) -> bool:
    return data.get("status") == MailingStatus.SCHEDULED


window = Window(
    Format(TEMPLATE_MESSAGE),
    Button(
        Const("Отменить отправку"),
        id="change_url_value",
        on_click=start_with_data(state=CancelMailingSG.confirm, field="mailing_id"),
        when=when_,  # type: ignore[arg-type]
    ),
    BACK,
    state=MailingsSG.item,
    getter=get_mailing,
)
