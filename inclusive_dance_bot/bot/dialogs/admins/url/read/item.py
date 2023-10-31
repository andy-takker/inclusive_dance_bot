from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    ChangeUrlSG,
    DeleteUrlSG,
    ReadUrlSG,
)
from inclusive_dance_bot.bot.dialogs.utils.start_with_data import StartWithData
from inclusive_dance_bot.services.storage import Storage


async def get_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "url": await storage.get_url_by_slug(dialog_manager.dialog_data["url_slug"])
    }


window = Window(
    Format("Ссылка {url.id}\n\nСлаг: {url.slug}\nЗначение: {url.value}"),
    StartWithData(
        Const("Изменить слаг"),
        id="change_url_slug",
        state=ChangeUrlSG.change_slug,
        keys=("url_slug",),
    ),
    StartWithData(
        Const("Изменить значение"),
        id="change_url_value",
        state=ChangeUrlSG.change_value,
        keys=("url_slug",),
    ),
    StartWithData(
        Const("Удалить ссылку"),
        id="delete_url",
        state=DeleteUrlSG.confirm,
        keys=("url_slug",),
    ),
    Back(Const("Назад")),
    state=ReadUrlSG.item,
    getter=get_data,
)
