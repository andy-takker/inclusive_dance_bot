from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    AdminSubmenuSG,
    FeedbackItemsSG,
    MailingsSG,
    ManageAdminSG,
    ReadUrlSG,
)
from idb.db.uow import UnitOfWork
from idb.generals.models.user import BotUser

MESSAGE_TEMPLATE = """
В боте зарегистрировано {total_users_count} пользователей.

Получено всего {total_feedbacks_count} ОС.

Запланировано/отправлено всего {total_mailings_count} рассылок.
"""


def when_(data: dict, widget: Any, dialog_manager: DialogManager) -> bool:
    user: BotUser = data["middleware_data"]["user"]
    return user.is_superuser


async def get_user_stat(
    dialog_manager: DialogManager, uow: UnitOfWork, **kwargs: Any
) -> dict[str, Any]:
    total_users_count = await uow.users.total_count()
    total_feedbacks_count = await uow.feedbacks.total_count()
    total_mailings_count = await uow.mailings.total_count()
    return {
        "total_users_count": total_users_count,
        "total_feedbacks_count": total_feedbacks_count,
        "total_mailings_count": total_mailings_count,
    }


window = Window(
    Const("Меню администратора"),
    Format(MESSAGE_TEMPLATE),
    Start(
        id="feedbacks",
        text=Const("🖋 Обратная связь от пользователей"),
        state=FeedbackItemsSG.menu,
    ),
    Start(
        id="mailings",
        text=Const("📬 Рассылки"),
        state=MailingsSG.menu,
    ),
    Start(
        id="manage_submenu_id",
        text=Const("📑 Управление подменю"),
        state=AdminSubmenuSG.items,
    ),
    Start(
        id="manage_url_id",
        text=Const("🔗 Управление ссылками"),
        state=ReadUrlSG.items,
    ),
    Start(
        id="manage_admin_id",
        text=Const("👮‍♀️ Управление администраторами"),
        state=ManageAdminSG.items,
        when=when_,
    ),
    state=AdminMainMenuSG.menu,
    getter=get_user_stat,
)
