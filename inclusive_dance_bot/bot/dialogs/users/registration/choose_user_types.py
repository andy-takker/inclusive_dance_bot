from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Multiselect, Next, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.messages import CHOOSE_USER_TYPE_MESSAGE
from inclusive_dance_bot.bot.dialogs.users.states import RegistrationSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.enums import RegistrationField
from inclusive_dance_bot.logic.storage import Storage


async def get_user_types_data(
    dialog_manager: DialogManager, storage: Storage, **kwargs: Any
) -> dict[str, Any]:
    user_types = await storage.get_user_types()
    return {
        "user_types": user_types.values(),
        RegistrationField.NAME: dialog_manager.dialog_data[RegistrationField.NAME],
    }


async def save_data(
    c: CallbackQuery,
    widget: Button,
    manager: DialogManager,
) -> None:
    ids: list[int] = manager.find("s_user_types").get_checked()  # type: ignore[union-attr]
    manager.dialog_data[RegistrationField.USER_TYPE_IDS] = ids


window = Window(
    Format(CHOOSE_USER_TYPE_MESSAGE),
    ScrollingGroup(
        Multiselect(
            checked_text=Format("\U00002705 {item.name}"),
            unchecked_text=Format("{item.name}"),
            id="s_user_types",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            items="user_types",
        ),
        id="user_types",
        width=1,
        height=10,
    ),
    BACK,
    Next(text=Const("Далее"), on_click=save_data),
    state=RegistrationSG.choose_types,
    getter=get_user_types_data,
)
