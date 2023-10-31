from collections.abc import Sequence

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import Data, StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.kbd.button import Button, OnClick
from aiogram_dialog.widgets.text import Text


class StartWithData(Start):
    def __init__(
        self,
        text: Text,
        id: str,
        state: State,
        data: Data = None,
        on_click: OnClick | None = None,
        mode: StartMode = StartMode.NORMAL,
        when: WhenCondition = None,
        keys: Sequence[str] = tuple(),
    ):
        self.transitional_data_keys = keys
        super().__init__(text, id, state, data, on_click, mode, when)

    async def _on_click(
        self, callback: CallbackQuery, button: Button, manager: DialogManager
    ) -> None:
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)
        data = {
            key: manager.dialog_data.get(key) for key in self.transitional_data_keys
        }
        if isinstance(self.start_data, dict):
            data.update(self.start_data)
        await manager.start(self.state, data, self.mode)
