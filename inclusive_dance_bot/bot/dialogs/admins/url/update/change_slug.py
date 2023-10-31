from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import ChangeUrlSG
from inclusive_dance_bot.bot.dialogs.admins.url.utils import get_url_data
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.exceptions.url import UrlSlugAlreadyExistsError
from inclusive_dance_bot.services.storage import Storage
from inclusive_dance_bot.services.update_data import update_url_by_slug
from inclusive_dance_bot.utils import check_slug

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
    storage: Storage = dialog_manager.middleware_data["storage"]
    try:
        await update_url_by_slug(
            uow=uow, storage=storage, url_slug=url_slug, slug=value
        )
    except UrlSlugAlreadyExistsError:
        dialog_manager.show_mode = ShowMode.SEND
        await message.answer(text="Такой слаг уже занят. Придумайте другой")
        return
    await dialog_manager.done(result={"url_slug": value})


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_slug", on_success=on_success),  # type: ignore[arg-type]
    Cancel(text=Const("Назад")),
    state=ChangeUrlSG.change_slug,
    getter=get_url_data,
)
