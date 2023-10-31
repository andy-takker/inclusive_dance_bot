from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.services.storage import Storage


class SubmenuListWindow(Window):
    def __init__(self, state: State) -> None:
        submenu_sg = self.get_submenu_kbd()

        super().__init__(
            Format("{message}"),
            submenu_sg,
            Cancel(Const("Назад")),
            state=state,
            getter=self.get_submenu_data,
        )

    def get_submenu_kbd(self) -> Column:
        return Column(
            Select(
                text=Format("{item.text}"),
                id="s_entities",
                item_id_getter=lambda x: x.id,
                type_factory=int,
                items="entities",
                on_click=self.open_message,  # type: ignore[arg-type]
            )
        )

    async def get_submenu_data(
        self, dialog_manager: DialogManager, storage: Storage, **kwargs: Any
    ) -> dict[str, Any]:
        submenu_type = dialog_manager.dialog_data["submenu_type"]
        submenus = await storage.get_submenus()
        return {
            "submenus": list(
                filter(lambda x: x.type == submenu_type, submenus.values())
            ),
            "message": dialog_manager.dialog_data["message"],
        }

    async def open_message(
        self,
        c: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        submenu_id: int,
    ) -> None:
        storage: Storage = dialog_manager.middleware_data["storage"]
        submenus = await storage.get_submenus()
        submenu = submenus[submenu_id]
        scrolling_text = dialog_manager.find("scroll_text")
        scrolling_text.widget.text = Format(submenu.message)  # type: ignore[union-attr]
        await dialog_manager.next()
