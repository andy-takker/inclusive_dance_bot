from typing import Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.users.states import FeedbackSG, SubmenuSG
from inclusive_dance_bot.enums import FeedbackType, SubmenuType
from inclusive_dance_bot.services.storage import Storage


class MainMenuWindow(Window):
    def __init__(self, state: State):
        self.submenu_type = SubmenuType.OTHER
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
                state=SubmenuSG.list_,
                data={
                    "message": "Принять участие в мероприятиях",
                    "submenu_type": SubmenuType.EVENT,
                },
            ),
            Start(
                id="education_id",
                text=Const("Пройти обучение"),
                state=SubmenuSG.list_,
                data={
                    "message": "Пройти обучение",
                    "submenu_type": SubmenuType.EDUCATION,
                },
            ),
            Start(
                id="enroll_id",
                text=Const("Записаться в студию"),
                state=SubmenuSG.list_,
                data={
                    "message": "Запись в студию",
                    "submenu_type": SubmenuType.ENROLL,
                },
            ),
            Start(
                id="charity_id",
                text=Const("Поддержать проект"),
                state=SubmenuSG.list_,
                data={
                    "message": "Поддержать проект",
                    "submenu_type": SubmenuType.CHARITY,
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
                    id="s_submenu",
                    item_id_getter=lambda x: x.id,
                    type_factory=int,
                    items="submenus",
                    on_click=self.open_message,  # type: ignore[arg-type]
                )
            ),
            Start(
                id="about_id",
                text=Const("Информация"),
                state=SubmenuSG.list_,
                data={
                    "message": "Информация о проекте",
                    "submenu_type": SubmenuType.INFORMATION,
                },
            ),
            state=state,
            getter=self.get_submenu_data,
        )

    async def get_submenu_data(self, storage: Storage, **kwargs: Any) -> dict[str, Any]:
        submenus = await storage.get_submenus()
        return {
            "submenus": list(
                filter(lambda x: x.type == self.submenu_type, submenus.values())
            ),
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
