from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    AdminMainMenuSG,
    DeleteUrlSG,
    ReadUrlSG,
)
from inclusive_dance_bot.bot.dialogs.admins.url.utils import get_url_data
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.delete_data import delete_url_by_slug
from inclusive_dance_bot.services.storage import Storage


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    url_slug = dialog_manager.start_data["url_slug"]
    await delete_url_by_slug(uow=uow, storage=storage, url_slug=url_slug)
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Ссылка была удалена")  # type: ignore[union-attr]
    await dialog_manager.start(state=AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)


dialog = Dialog(
    Window(
        Format("Вы действительно хотите удалить ссылку `{url.slug}`"),
        Row(
            Cancel(text=Const("Назад")),
            Button(text=Const("Удалить"), id="delete", on_click=on_click),
        ),
        state=DeleteUrlSG.confirm,
        getter=get_url_data,
    )
)
