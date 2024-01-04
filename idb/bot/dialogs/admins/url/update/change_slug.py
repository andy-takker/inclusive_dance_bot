from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from idb.bot.dialogs.admins.states import ChangeUrlSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_url_data
from idb.db.uow import UnitOfWork
from idb.exceptions.url import UrlSlugAlreadyExistsError
from idb.logic.url import update_url_by_slug
from idb.utils.cache import AbstractBotCache
from idb.utils.urls import check_slug

TEMPLATE_MESSAGE = (
    "Введите новый слаг\n(слаг может состоять только из латинских букв"
    " и символа подчеркивания) \n\nСтарый слаг: {url.slug}"
)


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    if not check_slug(value):
        dialog_manager.show_mode = ShowMode.SEND
        await message.answer(text="Некорректный слаг")
        return
    url_slug = dialog_manager.start_data["url_slug"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    try:
        await update_url_by_slug(uow=uow, cache=cache, url_slug=url_slug, slug=value)
    except UrlSlugAlreadyExistsError:
        dialog_manager.show_mode = ShowMode.SEND
        await message.answer(text="Такой слаг уже занят. Придумайте другой")
        return
    await dialog_manager.done(result={"url_slug": value})


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_slug", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=ChangeUrlSG.slug,
    getter=get_url_data,
)
