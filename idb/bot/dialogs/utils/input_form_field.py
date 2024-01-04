from collections.abc import Callable
from typing import Any

from aiogram import F
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.text import Const, Format


class InputFormWindow(Window):
    def __init__(
        self,
        state: State,
        message: str,
        field_name: str,
        is_first: bool = False,
        type_factory: Callable = str,
    ) -> None:
        self.message = message
        self.field_name = field_name
        self.is_first = is_first

        super().__init__(
            Format("{message}"),
            TextInput(
                id="text_input",
                on_success=self.on_success,  # type: ignore[arg-type]
                type_factory=type_factory,
            ),
            Cancel(text=Const("⬅️ Отмена"), when=F["is_first"]),
            Back(text=Const("⬅️ Назад"), when=~F["is_first"]),
            state=state,
            getter=self.get_data,
        )

    async def get_data(self, **kwargs: Any) -> dict[str, str | bool]:
        return {
            "is_first": self.is_first,
            "message": self.message,
        }

    async def on_success(
        self,
        message: Message,
        widget: TextInput,
        dialog_manager: DialogManager,
        value: str,
    ) -> None:
        dialog_manager.dialog_data[self.field_name] = value
        await dialog_manager.next()
