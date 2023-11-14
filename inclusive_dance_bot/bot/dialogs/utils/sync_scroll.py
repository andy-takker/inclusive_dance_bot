from collections.abc import Awaitable, Callable

from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.common.scroll import ManagedScroll


def sync_scroll(
    scroll_id: str,
) -> Callable[[ChatEvent, ManagedScroll, DialogManager], Awaitable[None],]:
    async def on_page_changed(
        event: ChatEvent,
        widget: ManagedScroll,
        dialog_manager: DialogManager,
    ) -> None:
        page = await widget.get_page()
        other_scroll: ManagedScroll = dialog_manager.find(
            scroll_id
        )  # type: ignore[assignment]
        await other_scroll.set_page(page=page)

    return on_page_changed
