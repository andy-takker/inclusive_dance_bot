from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateUrlSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.utils.cache import AbstractBotCache
from idb.utils.urls import check_slug


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, slug: str
) -> None:
    if not check_slug(slug):
        dialog_manager.show_mode = ShowMode.SEND
        await message.answer(text="Некорректный слаг")
        return

    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]

    try:
        await cache.get_url_by_slug(slug)
    except KeyError:
        dialog_manager.dialog_data["slug"] = slug
        await dialog_manager.next()
    else:
        dialog_manager.show_mode = ShowMode.SEND
        await message.answer(text="Такой слаг уже занят. Придумайте другой")
        return


window = Window(
    Const("Введите слаг для новой ссылки"),
    TextInput(id="input_slug", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=CreateUrlSG.slug,
)
