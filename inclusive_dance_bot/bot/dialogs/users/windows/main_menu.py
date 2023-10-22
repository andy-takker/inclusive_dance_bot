from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.states import EntitySG, FeedbackSG
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import EntityType, FeedbackType
from inclusive_dance_bot.services.storage import Storage


class MainMenuWindow(Window):
    def __init__(self, state: State):
        self.entity_type = EntityType.SUBMENU
        super().__init__(
            Const("Главное меню"),
            Start(
                id="place_ad_id",
                text=Const("Разместить объявление"),
                state=FeedbackSG.input_title,
                data={
                    "type": FeedbackType.ADVERTISEMENT,
                },
            ),
            Start(
                id="education_id",
                text=Const("Принять участие в мероприятиях"),
                state=EntitySG.list_,
                data={
                    "message": "Принять участие в мероприятиях",
                    "entity_type": EntityType.EVENT,
                },
            ),
            Start(
                id="education_id",
                text=Const("Пройти обучение"),
                state=EntitySG.list_,
                data={
                    "message": "Пройти обучение",
                    "entity_type": EntityType.EDUCATION,
                },
            ),
            Start(
                id="enroll_id",
                text=Const("Записаться в студию"),
                state=EntitySG.list_,
                data={
                    "message": "Запись в студию",
                    "entity_type": EntityType.ENROLL,
                },
            ),
            Start(
                id="charity_id",
                text=Const("Поддержать проект"),
                state=EntitySG.list_,
                data={
                    "message": "Поддержать проект",
                    "entity_type": EntityType.CHARITY,
                },
            ),
            Start(
                id="ask_id",
                text=Const("Задать вопрос / внести предложение"),
                state=FeedbackSG.input_title,
                data={"type": FeedbackType.QUESTION},
            ),
            Column(
                Select(
                    text=Format("{item.text}"),
                    id="s_entities",
                    item_id_getter=lambda x: x.id,
                    type_factory=int,
                    items="entities",
                    on_click=self.open_message,  # type: ignore[arg-type]
                )
            ),
            Start(
                id="about_id",
                text=Const("Информация"),
                state=EntitySG.list_,
                data={
                    "message": "Информация о проекте",
                    "entity_type": EntityType.INFORMATION,
                },
            ),
            state=state,
            getter=self.get_entities_data,
        )

    async def get_entities_data(
        self, storage: Storage, **kwargs: Any
    ) -> dict[str, Any]:
        entities = await storage.get_entities()
        return {
            "entities": list(
                filter(lambda x: x.type == self.entity_type, entities.values())
            ),
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
        scrolling_text = dialog_manager.find("scroll_text")
        scrolling_text.widget.text = Format(entity.message)  # type: ignore[union-attr]
        await dialog_manager.next()
