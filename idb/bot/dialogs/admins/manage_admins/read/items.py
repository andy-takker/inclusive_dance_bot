from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import (
    AddAdminSG,
    DeleteAdminSG,
    ManageAdminSG,
)
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork


async def get_admins(uow: UnitOfWork, **kwargs: Any) -> dict[str, Any]:
    admins = await uow.users.get_admin_list(include_superusers=False)

    return {"admins": admins}


async def on_click(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, user_id: int
) -> None:
    await dialog_manager.start(state=DeleteAdminSG.confirm, data={"user_id": user_id})


window = Window(
    Const("Администраторы"),
    ScrollingGroup(
        Select(
            Format("@{item.username}"),
            id="admins_s",
            item_id_getter=lambda x: x.id,
            items="admins",
            on_click=on_click,  # type: ignore[arg-type]
            type_factory=int,
        ),
        id="admin_list",
        height=10,
        hide_on_single_page=True,
    ),
    Start(
        text=Const("💻 Назначить администратора"),
        id="add_admin",
        state=AddAdminSG.input_username,
    ),
    CANCEL,
    getter=get_admins,
    state=ManageAdminSG.items,
)
