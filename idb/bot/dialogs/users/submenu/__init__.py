from typing import Any

from aiogram_dialog import Dialog, DialogManager

from idb.bot.dialogs.users.states import SubmenuSG
from idb.bot.dialogs.users.submenu import submenu_list
from idb.bot.dialogs.utils.submenu_window import SubmenuWindow


async def on_start(data: dict[str, Any], dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data["message"] = data["message"]
    dialog_manager.dialog_data["type"] = data["type"]


dialog = Dialog(
    submenu_list.window,
    SubmenuWindow(SubmenuSG.submenu),
    on_start=on_start,
)
# 292990139,
