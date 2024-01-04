from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CreateSubmenuSG
from idb.bot.dialogs.utils.buttons import BACK

TEMPLATE_MESSAGE = (
    "Введите вес подменю.\n\n"
    "Вес влияет на порядок отображения. Больше вес - выше в списке."
)


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, weight: int
) -> None:
    dialog_manager.dialog_data["weight"] = weight
    await dialog_manager.next()


window = Window(
    Const(TEMPLATE_MESSAGE),
    TextInput(id="input_weight", on_success=on_success, type_factory=int),  # type: ignore[arg-type]
    BACK,
    state=CreateSubmenuSG.weight,
)
