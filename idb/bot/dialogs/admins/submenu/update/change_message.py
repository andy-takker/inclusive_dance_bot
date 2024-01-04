from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Jinja

from idb.bot.dialogs.admins.states import ChangeSubmenuSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.bot.dialogs.utils.getters import get_submenu_data
from idb.db.uow import UnitOfWork
from idb.logic.submenu import update_submenu_by_id
from idb.utils.cache import AbstractBotCache

TEMPLATE_MESSAGE = (
    "Введите новый шаблон сообщения\nТекущее:\n\n<code>{{submenu.message}}</code>"
)


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
        message=value,
    )
    await dialog_manager.done()


window = Window(
    Jinja(TEMPLATE_MESSAGE),
    TextInput(id="input_message", on_success=on_success),  # type: ignore[arg-type]
    CANCEL,
    state=ChangeSubmenuSG.message,
    getter=get_submenu_data,
)
