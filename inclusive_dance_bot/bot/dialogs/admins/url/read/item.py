from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import (
    ChangeUrlSG,
    DeleteUrlSG,
    ReadUrlSG,
)
from inclusive_dance_bot.bot.dialogs.messages import URL_TEMPLATE
from inclusive_dance_bot.bot.dialogs.utils import start_with_data
from inclusive_dance_bot.logic.storage import Storage

URL_ID = "url_slug"


async def get_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {"url": await storage.get_url_by_slug(dialog_manager.dialog_data[URL_ID])}


window = Window(
    Format(URL_TEMPLATE),
    Button(
        Const("Изменить слаг"),
        id="change_url_slug",
        on_click=start_with_data(state=ChangeUrlSG.slug, field=URL_ID),
    ),
    Button(
        Const("Изменить значение"),
        id="change_url_value",
        on_click=start_with_data(state=ChangeUrlSG.value, field=URL_ID),
    ),
    Button(
        Const("Удалить ссылку"),
        id="delete_url",
        on_click=start_with_data(state=DeleteUrlSG.confirm, field=URL_ID),
    ),
    Back(Const("Назад")),
    state=ReadUrlSG.item,
    getter=get_data,
)
