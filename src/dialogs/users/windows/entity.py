from typing import Any

from aiogram.fsm.state import State
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, NumberedPager
from aiogram_dialog.widgets.text import Const, Format, ScrollingText

from src.middlewares.cache import CacheStorage


def when_(data: dict, widget: NumberedPager, dialog_manager: DialogManager) -> bool:
    return data.get("pages", 1) > 1


class EntityWindow(Window):
    def __init__(self, state: State):
        super().__init__(
            ScrollingText(text=Format("default"), id="scroll_text", page_size=1000),
            NumberedPager(scroll="scroll_text", when=when_),  # type: ignore[arg-type]
            Back(text=Const("Назад")),
            state=state,
            getter=self.get_cache_data,
        )

    @staticmethod
    async def get_cache_data(cache: CacheStorage, **kwargs: Any) -> dict[str, Any]:
        return cache._storage
