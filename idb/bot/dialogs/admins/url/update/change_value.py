from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from idb.bot.dialogs.admins.states import ChangeUrlSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_url_data
from idb.db.uow import UnitOfWork
from idb.logic.url import update_url_by_slug
from idb.utils.cache import AbstractBotCache

TEMPLATE_MESSAGE = "Введите новое значение ссылки\n\nТекущее: {url.value}"


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    url_slug = dialog_manager.start_data["url_slug"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    await update_url_by_slug(uow=uow, cache=cache, url_slug=url_slug, value=value)

    await dialog_manager.done(result={"url_slug": url_slug})


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_value", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=ChangeUrlSG.value,
    getter=get_url_data,
)
