from collections.abc import Awaitable, Callable

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd.button import Button


def start_with_data(
    state: State, field: str, mode: StartMode = StartMode.NORMAL
) -> Callable[[CallbackQuery, Button, DialogManager], Awaitable[None]]:
    async def on_click(
        callback: CallbackQuery, button: Button, manager: DialogManager
    ) -> None:
        data = {field: manager.dialog_data.get(field)}
        await manager.start(state, data, mode=mode)

    return on_click
