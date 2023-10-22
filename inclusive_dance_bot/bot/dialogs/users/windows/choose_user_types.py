from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Multiselect, Next, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.messages import CHOOSE_USER_TYPE_MESSAGE
from inclusive_dance_bot.services.storage import Storage


class ChooseUserTypesWindow(Window):
    def __init__(self, state: State):
        user_types_sg = self.get_user_types_kbd()
        super().__init__(
            Format(CHOOSE_USER_TYPE_MESSAGE),
            user_types_sg,
            Back(text=Const("Назад")),
            Next(text=Const("Сохранить"), on_click=save_user_types),
            getter=get_choose_user_types_data,
            state=state,
        )

    def get_user_types_kbd(self) -> ScrollingGroup:
        ms: Multiselect = Multiselect(
            checked_text=Format("\U00002705 {item.name}"),
            unchecked_text=Format("{item.name}"),
            id="s_user_types",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            items="user_types",
        )
        return ScrollingGroup(
            ms,
            id="user_types",
            width=1,
            height=10,
        )


async def get_choose_user_types_data(
    dialog_manager: DialogManager, storage: Storage, **kwargs: Any
) -> dict[str, Any]:
    user_types = await storage.get_user_types()
    return {
        "user_types": user_types.values(),
        "name": dialog_manager.dialog_data["name"],
    }


async def save_user_types(
    c: CallbackQuery, widget: Button, manager: DialogManager
) -> None:
    manager.dialog_data["user_type_ids"] = manager.find("s_user_types").get_checked()  # type: ignore[union-attr]
