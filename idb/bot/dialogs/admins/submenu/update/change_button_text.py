from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from idb.bot.dialogs.admins.states import ChangeSubmenuSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_submenu_data
from idb.bot.dialogs.utils.validators import validate_length
from idb.db.uow import UnitOfWork
from idb.logic.submenu import update_submenu_by_id
from idb.utils.cache import AbstractBotCache

TEMPLATE_MESSAGE = "Введите новый текст кнопки\n\nТекущее: {submenu.button_text}"


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    submenu_id = dialog_manager.start_data["submenu_id"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    await update_submenu_by_id(
        uow=uow,
        cache=cache,
        submenu_id=submenu_id,
        button_text=value,
    )
    await dialog_manager.done()


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(
        id="input_button_text",
        on_success=on_success,  # type: ignore[arg-type]
        type_factory=validate_length(64),
    ),
    CANCEL,
    state=ChangeSubmenuSG.button_text,
    getter=get_submenu_data,
)
