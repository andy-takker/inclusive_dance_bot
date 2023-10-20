from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from src.db.uow.main import UnitOfWork
from src.enums import EntityType
from src.states import EntitySG


class MainMenuWindow(Window):
    def __init__(self, state: State):
        self.entity_type = EntityType.SUBMENU
        entities_kbd = self.get_entities_kbd()

        super().__init__(
            Const("Главное меню"),
            Start(id="place_ad_id", text=Const("Разместить объявление"), state=None),
            Start(
                id="education_id",
                text=Const("Принять участие в мероприятиях"),
                state=EntitySG.list_,
                data={
                    "message": "Принять участие в мероприятиях",
                    "entity": EntityType.EVENT,
                },
            ),
            Start(
                id="education_id",
                text=Const("Пройти обучение"),
                state=EntitySG.list_,
                data={
                    "message": "Пройти обучение",
                    "entity": EntityType.EDUCATION,
                },
            ),
            Start(
                id="enroll_id",
                text=Const("Записаться в студию"),
                state=EntitySG.list_,
                data={
                    "message": "Запись в студию",
                    "entity": EntityType.ENROLL,
                },
            ),
            Start(
                id="charity_id",
                text=Const("Поддержать проект"),
                state=EntitySG.list_,
                data={
                    "message": "Поддержать проект",
                    "entity": EntityType.CHARITY,
                },
            ),
            Start(
                id="ask_id",
                text=Const("Задать вопрос / внести предложение"),
                state=None,
            ),
            entities_kbd,
            Start(
                id="about_id",
                text=Const("Информация"),
                state=EntitySG.list_,
                data={
                    "message": "Информация о проекте",
                    "entity": EntityType.INFORMATION,
                },
            ),
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
