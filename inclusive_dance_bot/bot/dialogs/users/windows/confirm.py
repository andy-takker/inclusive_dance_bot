from aiogram.fsm.state import State
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, NumberedPager
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Format, ScrollingText
from aiogram_dialog.widgets.utils import GetterVariant


class ConfirmWindow(Window):
    def __init__(
        self,
        state: State,
        format_template: str,
        on_click: OnClick,
        getter: GetterVariant,
        confirm_button_text: str | None = None,
    ):
        if confirm_button_text is None:
            confirm_button_text = "Сохранить"
        super().__init__(
            ScrollingText(
                text=Format(text=format_template), id="scroll_text", page_size=1000
            ),
            NumberedPager(scroll="scroll_text", when=when_),  # type: ignore[arg-type]
            Back(Const("Назад")),
            Button(Const(confirm_button_text), id="confirm", on_click=on_click),
            state=state,
            getter=getter,
        )


def when_(data: dict, widget: NumberedPager, dialog_manager: DialogManager) -> bool:
    return data.get("pages", 1) > 1
