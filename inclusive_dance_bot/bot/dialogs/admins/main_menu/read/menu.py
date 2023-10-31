from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminFeedbackSG,
    AdminMainMenuSG,
    AdminManageAdminSG,
    AdminSendMessageSG,
    AdminSubmenuSG,
    ReadUrlSG,
)
from inclusive_dance_bot.services.user_controller import MegaUser


def when_(data: dict, widget: Any, dialog_manager: DialogManager) -> bool:
    user: MegaUser = data["middleware_data"]["user"]
    return user.is_superuser


window = Window(
    Const("Меню администратора"),
    Format("*Здесь должна быть статистика по пользователям*"),
    Start(
        id="feedback_id",
        text=Const("Обратная связь от пользователей"),
        state=AdminFeedbackSG.items,
    ),
    Start(
        id="send_message",
        text=Const("Отправить сообщение пользователям"),
        state=AdminSendMessageSG.choose_user_types,
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
        state=AdminManageAdminSG.items,
        when=when_,
    ),
    state=AdminMainMenuSG.menu,
)
