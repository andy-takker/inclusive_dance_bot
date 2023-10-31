from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import CreateUrlSG, ReadUrlSG
from inclusive_dance_bot.services.storage import Storage

SCROLL_ID = "url_scroll_id"


async def get_urls_list_data(storage: Storage, **kwargs: Any) -> dict[str, Any]:
    return {"urls": (await storage.get_urls()).values()}


async def open_url(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, url_slug: int
) -> None:
    dialog_manager.dialog_data["url_slug"] = url_slug
    await dialog_manager.next()


window = Window(
    Const("Ссылки"),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_url",
            item_id_getter=lambda x: x.slug,
            items="urls",
            on_click=open_url,  # type: ignore[arg-type]
        ),
        id=SCROLL_ID,
        width=5,
        height=3,
    ),
    Start(
        text=Const("Добавить ссылку"),
        id="create_url",
        state=CreateUrlSG.input_slug,
    ),
    Cancel(text=Const("Назад")),
    state=ReadUrlSG.items,
    getter=get_urls_list_data,
)
