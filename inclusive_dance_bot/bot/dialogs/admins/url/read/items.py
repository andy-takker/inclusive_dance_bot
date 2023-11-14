from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format, List

from inclusive_dance_bot.bot.dialogs.admins.states import CreateUrlSG, ReadUrlSG
from inclusive_dance_bot.bot.dialogs.utils import sync_scroll
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.logic.storage import Storage

SCROLL_KBD_ID = "url_scroll_id"
SCROLL_MESSAGE_ID = "url_message_scroll_id"


async def get_urls_list_data(storage: Storage, **kwargs: Any) -> dict[str, Any]:
    return {"urls": list((await storage.get_urls()).values())}


async def open_url(
    c: CallbackQuery, widget: Button, dialog_manager: DialogManager, url_slug: int
) -> None:
    dialog_manager.dialog_data["url_slug"] = url_slug
    await dialog_manager.next()


window = Window(
    Const("Ссылки\n"),
    List(
        Format("[{pos}]  {item.slug}"),
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
