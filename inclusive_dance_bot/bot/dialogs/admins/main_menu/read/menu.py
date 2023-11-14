from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminFeedbackSG,
    AdminMainMenuSG,
    AdminSubmenuSG,
    MailingsSG,
    ManageAdminSG,
    ReadUrlSG,
)
from inclusive_dance_bot.logic.user import MegaUser


def when_(data: dict, widget: Any, dialog_manager: DialogManager) -> bool:
    user: MegaUser = data["middleware_data"]["user"]
    return user.is_superuser


window = Window(
    Const("Меню администратора"),
    Format("*Здесь должна быть статистика по пользователям*"),
    Start(
        id="feedbacks",
        text=Const("Обратная связь от пользователей"),
        state=AdminFeedbackSG.items,
    ),
    Start(
        id="mailings",
        text=Const("Рассылки"),
        state=MailingsSG.menu,
    ),
    Start(
        id="manage_submenu_id",
        text=Const("Управление подменю"),
        state=AdminSubmenuSG.items,
    ),
    Start(
        id="manage_url_id",
        text=Const("Управление ссылками"),
        state=ReadUrlSG.items,
    ),
    Start(
        id="manage_admin_id",
        text=Const("Управление администраторами"),
        state=ManageAdminSG.items,
        when=when_,
    ),
    state=AdminMainMenuSG.menu,
)
