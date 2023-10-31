from typing import Any

from aiogram_dialog import Dialog, DialogManager

from inclusive_dance_bot.bot.dialogs.users.states import SubmenuSG
from inclusive_dance_bot.bot.dialogs.users.windows.submenu import SubmenuWindow
from inclusive_dance_bot.bot.dialogs.users.windows.submenu_list import SubmenuListWindow


class SubmenuDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            SubmenuListWindow(state=SubmenuSG.list_),
            SubmenuWindow(state=SubmenuSG.submenu),
            on_start=self.custom_on_start,
        )

    async def custom_on_start(
        self, data: dict[str, Any], dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data["message"] = data["message"]
        dialog_manager.dialog_data["submenu_type"] = data["submenu_type"]
