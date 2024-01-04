from typing import Any

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.admins.states import (
    ChangeUrlSG,
    DeleteUrlSG,
    ReadUrlSG,
)
from idb.bot.dialogs.messages import URL_TEMPLATE
from idb.bot.dialogs.utils import start_with_data
from idb.bot.dialogs.utils.buttons import BACK
from idb.utils.cache import AbstractBotCache

URL_ID = "url_slug"


async def get_data(
    cache: AbstractBotCache, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {"url": await cache.get_url_by_slug(dialog_manager.dialog_data[URL_ID])}


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
    BACK,
    state=ReadUrlSG.item,
    getter=get_data,
)
