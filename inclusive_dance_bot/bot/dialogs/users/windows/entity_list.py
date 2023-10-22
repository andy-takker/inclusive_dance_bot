from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.services.storage import Storage


class EntityListWindow(Window):
    def __init__(self, state: State) -> None:
        entities_sg = self.get_entities_kbd()

        super().__init__(
            Format("{message}"),
            entities_sg,
            Cancel(Const("Назад")),
            state=state,
            getter=self.get_entities_data,
        )

    def get_entities_kbd(self) -> Column:
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

    async def get_entities_data(
        self, dialog_manager: DialogManager, storage: Storage, **kwargs: Any
    ) -> dict[str, Any]:
        entity_type = dialog_manager.dialog_data["entity_type"]
        entities = await storage.get_entities()
        return {
            "entities": list(
                filter(lambda x: x.type == entity_type, entities.values())
            ),
            "message": dialog_manager.dialog_data["message"],
        }

    async def open_message(
        self,
        c: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        entity_id: int,
    ) -> None:
        storage: Storage = dialog_manager.middleware_data["storage"]
        entities = await storage.get_entities()
        entity = entities[entity_id]
        scrolling_text = dialog_manager.find("scroll_text")
        scrolling_text.widget.text = Format(entity.message)  # type: ignore[union-attr]
        await dialog_manager.next()
