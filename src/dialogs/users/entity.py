from typing import Any

from aiogram_dialog import Dialog, DialogManager

from src.dialogs.users.windows.entities import EntitiesWindow2
from src.dialogs.users.windows.entity import EntityWindow
from src.states import EntitySG


class EntityDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            EntitiesWindow2(state=EntitySG.list_),
            EntityWindow(state=EntitySG.entity),
            on_start=self.custom_on_start,
        )

    async def custom_on_start(
        self, data: dict[str, Any], dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data["message"] = data["message"]
        dialog_manager.dialog_data["entity"] = data["entity"]
