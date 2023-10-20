from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from src.db.uow.main import UnitOfWork
from src.enums import EntityType


class EntitiesWindow(Window):
    def __init__(
        self, state: State, entity_type: EntityType, message: str = "Default"
    ) -> None:
        self.entity_type = entity_type

        entities_sg = self.get_entities_kbd()

        super().__init__(
            Const(message),
            entities_sg,
            Cancel(Const("Назад")),
            state=state,
            getter=self.get_entities_data,
        )

    def get_entities_kbd(self) -> Column:
        s = Select(
            text=Format("{item.text}"),
            id="s_entities",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            items="entities",
            on_click=self.open_message,  # type: ignore[arg-type]
        )
        return Column(s)

    async def get_entities_data(self, uow: UnitOfWork, **kwargs: Any) -> dict[str, Any]:
        entities = await uow.entities.get_entities_by_type(entity_type=self.entity_type)
        return {
            "entities": entities,
        }

    async def open_message(
        self,
        c: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        entity_id: int,
    ) -> None:
        uow: UnitOfWork = dialog_manager.middleware_data["uow"]
        entity = await uow.entities.get_entity_by_id(entity_id=entity_id)
        dialog_manager.find("scroll_text").widget.text = Format(entity.message)  # type: ignore[union-attr]
        await dialog_manager.next()


class EntitiesWindow2(Window):
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
        self, dialog_manager: DialogManager, uow: UnitOfWork, **kwargs: Any
    ) -> dict[str, Any]:
        entities = await uow.entities.get_entities_by_type(
            entity_type=dialog_manager.dialog_data["entity"]
        )
        return {
            "entities": entities,
            "message": dialog_manager.dialog_data["message"],
        }

    async def open_message(
        self,
        c: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        entity_id: int,
    ) -> None:
        uow: UnitOfWork = dialog_manager.middleware_data["uow"]
        entity = await uow.entities.get_entity_by_id(entity_id=entity_id)
        dialog_manager.find("scroll_text").widget.text = Format(entity.message)  # type: ignore[union-attr]
        await dialog_manager.next()
