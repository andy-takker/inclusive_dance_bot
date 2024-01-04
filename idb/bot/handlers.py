import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager

from idb.bot.utils import start_new_dialog

log = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    """Example of handling UnknownIntent Error and starting new dialog."""
    log.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот был перезапущен для тех. обслуживания.\n"
            "Вы будете перенаправлены в главное меню.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    await start_new_dialog(dialog_manager=dialog_manager)


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    """Example of handling UnknownState Error and starting new dialog."""
    log.error("Restarting dialog: %s", event.exception)
    await start_new_dialog(dialog_manager=dialog_manager)
