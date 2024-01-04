from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.messages import INPUT_REGION_MESSAGE
from idb.bot.dialogs.users.states import RegistrationSG
from idb.bot.dialogs.utils.buttons import BACK


async def on_success(
    message: Message, widget: TextInput, dialog_manager: DialogManager, value: str
) -> None:
    dialog_manager.dialog_data["region"] = value
    await dialog_manager.next()


window = Window(
    Const(INPUT_REGION_MESSAGE),
    TextInput("input_region_id", on_success=on_success),  # type: ignore[arg-type]
    BACK,
    state=RegistrationSG.input_region,
)
