from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import AdminMainMenuSG, DeleteUrlSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_url_data
from idb.db.uow import UnitOfWork
from idb.logic.url import delete_url_by_slug
from idb.utils.cache import AbstractBotCache


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    url_slug = dialog_manager.start_data["url_slug"]
    await delete_url_by_slug(uow=uow, cache=cache, url_slug=url_slug)
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Ссылка была удалена")  # type: ignore[union-attr]
    await dialog_manager.start(state=AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)


window = Window(
    Format("Вы действительно хотите удалить ссылку `{url.slug}`?"),
    Row(
        CANCEL,
        Button(text=Const("Удалить"), id="delete_url", on_click=on_click),
    ),
    state=DeleteUrlSG.confirm,
    getter=get_url_data,
)
