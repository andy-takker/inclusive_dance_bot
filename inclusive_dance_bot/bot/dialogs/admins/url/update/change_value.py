from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.admins.states import ChangeUrlSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.bot.dialogs.utils.getters import get_url_data
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.url import update_url_by_slug

TEMPLATE_MESSAGE = "Введите новое значение ссылки\n\nТекущее: {url.value}"


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    url_slug = dialog_manager.start_data["url_slug"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    storage: Storage = dialog_manager.middleware_data["storage"]
    await update_url_by_slug(uow=uow, storage=storage, url_slug=url_slug, value=value)

    await dialog_manager.done(result={"url_slug": url_slug})


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_value", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=ChangeUrlSG.value,
    getter=get_url_data,
)
