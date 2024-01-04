from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Start
from aiogram_dialog.widgets.text import Const, Format

from idb.bot.dialogs.users.states import (
    FeedbackSG,
    MainMenuSG,
    SubmenuSG,
)
from idb.generals.enums import FeedbackType, SubmenuType
from idb.utils.cache import AbstractBotCache


async def get_submenus_data(cache: AbstractBotCache, **kwargs: Any) -> dict[str, Any]:
    submenus = await cache.get_submenus()
    return {
        "submenus": list(
            filter(lambda x: x.type == SubmenuType.OTHER, submenus.values())
        ),
    }


async def open_message(
    c: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    submenu_id: int,
) -> None:
    cache: AbstractBotCache = dialog_manager.middleware_data["cache"]
    submenus = await cache.get_submenus()
    submenu = submenus[submenu_id]
    scrolling_text = dialog_manager.find("scroll_text")
    scrolling_text.widget.text = Format(submenu.message)  # type: ignore[union-attr]
    await dialog_manager.next()


window = Window(
    Const("Главное меню"),
    Start(
        id="create_ad_id",
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
            "type": SubmenuType.EVENT,
        },
    ),
    Start(
        id="education_id",
        text=Const("Пройти обучение"),
        state=SubmenuSG.list_,
        data={
            "message": "Пройти обучение",
            "type": SubmenuType.EDUCATION,
        },
    ),
    Start(
        id="enroll_id",
        text=Const("Записаться в студию"),
        state=SubmenuSG.list_,
        data={
            "message": "Запись в студию",
            "type": SubmenuType.ENROLL,
        },
    ),
    Start(
        id="charity_id",
        text=Const("Поддержать проект"),
        state=SubmenuSG.list_,
        data={
            "message": "Поддержать проект",
            "type": SubmenuType.CHARITY,
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
            text=Format("{item.button_text}"),
            id="s_submenu",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            items="submenus",
            on_click=open_message,  # type: ignore[arg-type]
        )
    ),
    Start(
        id="about_id",
        text=Const("Информация"),
        state=SubmenuSG.list_,
        data={
            "message": "Информация о проекте",
            "type": SubmenuType.INFORMATION,
        },
    ),
    state=MainMenuSG.menu,
    getter=get_submenus_data,
)
