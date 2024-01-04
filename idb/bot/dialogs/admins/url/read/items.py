from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format, List

from idb.bot.dialogs.admins.states import CreateUrlSG, ReadUrlSG
from idb.bot.dialogs.utils import sync_scroll
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.utils.cache import AbstractBotCache

SCROLL_KBD_ID = "url_scroll_id"
SCROLL_MESSAGE_ID = "url_message_scroll_id"


async def get_urls_list_data(cache: AbstractBotCache, **kwargs: Any) -> dict[str, Any]:
    return {"urls": list((await cache.get_urls()).values())}


async def open_url(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, url_slug: str
) -> None:
    dialog_manager.dialog_data["url_slug"] = url_slug
    await dialog_manager.next()


window = Window(
    Const("Ссылки\n"),
    List(
        Format("[{pos}] {item.slug}"),
        items="urls",
        id=SCROLL_MESSAGE_ID,
        page_size=10,
    ),
    ScrollingGroup(
        Select(
            Format("{pos}"),
            id="s_url",
            item_id_getter=lambda x: x.slug,
            items="urls",
            on_click=open_url,  # type: ignore[arg-type]
        ),
        id=SCROLL_KBD_ID,
        width=5,
        height=2,
        hide_on_single_page=True,
        on_page_changed=sync_scroll(SCROLL_MESSAGE_ID),
    ),
    Start(
        text=Const("Добавить ссылку"),
        id="create_url",
        state=CreateUrlSG.slug,
    ),
    CANCEL,
    state=ReadUrlSG.items,
    getter=get_urls_list_data,
)
