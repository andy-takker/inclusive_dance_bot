from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format

from inclusive_dance_bot.bot.dialogs.admins.states import ChangeSubmenuSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import CANCEL
from inclusive_dance_bot.bot.dialogs.utils.getters import get_submenu_data
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.submenu import update_submenu_by_id

TEMPLATE_MESSAGE = (
    "Введите новое значение веса. "
    "Вес влияет на порядок отображения. Больше вес - выше в списке."
    "\n\nТекущее: {submenu.weight}"
)


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, weight: int
) -> None:
    submenu_id = dialog_manager.start_data["submenu_id"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    storage: Storage = dialog_manager.middleware_data["storage"]
    await update_submenu_by_id(
        uow=uow, storage=storage, submenu_id=submenu_id, weight=weight
    )
    await dialog_manager.done()


window = Window(
    Format(TEMPLATE_MESSAGE),
    TextInput(id="input_weight", on_success=on_success, type_factory=int),  # type: ignore[arg-type]
    CANCEL,
    state=ChangeSubmenuSG.weight,
    getter=get_submenu_data,
)
