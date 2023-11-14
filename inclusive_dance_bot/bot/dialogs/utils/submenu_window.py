from typing import Any

from aiogram.fsm.state import State
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import NumberedPager
from aiogram_dialog.widgets.text import Format, ScrollingText

from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.logic.storage import Storage


class SubmenuWindow(Window):
    def __init__(self, state: State) -> None:
        super().__init__(
            ScrollingText(text=Format("default"), id="scroll_text", page_size=1000),
            NumberedPager(scroll="scroll_text", when=when_),  # type: ignore[arg-type]
            BACK,
            state=state,
            getter=self.get_urls,
        )

    async def get_urls(self, storage: Storage, **kwargs: Any) -> dict[str, Any]:
        return await storage.get_urls()


def when_(data: dict, widget: NumberedPager, dialog_manager: DialogManager) -> bool:
    return data.get("pages", 1) > 1
