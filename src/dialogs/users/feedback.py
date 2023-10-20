from typing import Any

from aiogram_dialog import Dialog, DialogManager

from src.dialogs.utils.input_form_field import InputFormWindow
from src.states import FeedbackSG


class FeedbackDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            InputFormWindow(
                state=FeedbackSG.input_title,
                message="Укажите тему обращения",
                field_name="title",
                is_first=True,
            ),
            InputFormWindow(
                state=FeedbackSG.input_title,
                message="Опишите Вашу проблему или предложение. Администраторы обязательно его расммотрят",
                field_name="text",
            ),
            ConfirmFeedbackWindow(state=FeedbackSG.confirm),
            on_start=self.custom_on_start,
        )

    async def custom_on_start(
        self, data: dict[str, Any], dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data["feedback"] = data["feedback"]
