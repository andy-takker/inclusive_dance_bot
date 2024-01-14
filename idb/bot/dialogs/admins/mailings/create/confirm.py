from datetime import date, datetime, time, timedelta, timezone
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import CreateMailingSG
from idb.bot.dialogs.utils.buttons import BACK
from idb.db.uow import UnitOfWork
from idb.logic.mailing import save_mailing
from idb.utils.cache import AbstractBotCache


def parse_dt(
    t: str | None,
    d: str | None,
) -> datetime | None:
    if t and d:
        return datetime.combine(
            date.fromisoformat(d),
            time.fromisoformat(t),
            tzinfo=timezone(offset=timedelta(hours=3)),
        )
    return None


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    t = dialog_manager.dialog_data.get("time")
    d = dialog_manager.dialog_data.get("date")
    scheduled_at = parse_dt(t=t, d=d)
    author_id: int = c.from_user.id
    await save_mailing(
        uow=uow,
        bot=dialog_manager.middleware_data["bot"],
        author_id=author_id,
        title=dialog_manager.dialog_data["title"],
        content=dialog_manager.dialog_data["content"],
        scheduled_at=None if not scheduled_at else scheduled_at,
        user_type_ids=dialog_manager.dialog_data["user_types"],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(author_id, text="Рассылка создана")  # type: ignore[union-attr]
    await dialog_manager.done()


async def get_mailing_data(
    dialog_manager: DialogManager, cache: AbstractBotCache, **kwargs: Any
) -> dict[str, Any]:
    user_types = filter(
        lambda ut: ut.id in dialog_manager.dialog_data["user_types"],
        (await cache.get_user_types()).values(),
    )
    t = dialog_manager.dialog_data.get("time")
    d = dialog_manager.dialog_data.get("date")
    dt = parse_dt(t=t, d=d)
    return {
        "title": dialog_manager.dialog_data["title"],
        "content": dialog_manager.dialog_data["content"],
        "user_types": ", ".join(map(lambda x: x.name, user_types)),
        "time": t,
        "date": d,
        "dt": dt,
        "is_immediately": t is None or d is None,
    }


window = Window(
    Format(
        "Рассылка\n\n"
        "Заголовок: <b>{title}</b>\n"
        "Основной текст: {content}\n"
        "Целевые пользователи: <i>{user_types}</i>\n"
    ),
    Format(
        "Дата и время отправки: <i>{dt:%H:%M %d.%m.%Y}</i>",
        when=~F["is_immediately"],
    ),
    Format("<i>Будет отправлено немедлено</i>", when=F["is_immediately"]),
    Row(
        BACK,
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=CreateMailingSG.confirm,
    getter=get_mailing_data,
)
