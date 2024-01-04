from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from idb.bot.dialogs.admins.states import CancelMailingSG
from idb.bot.dialogs.utils.buttons import CANCEL
from idb.db.uow import UnitOfWork
from idb.generals.enums import MailingStatus
from idb.logic.mailing import update_mailing_by_id


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    mailing_id = dialog_manager.start_data["mailing_id"]
    await update_mailing_by_id(
        uow=uow, mailing_id=mailing_id, status=MailingStatus.CANCELLED
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Рассылка была отменена")  # type: ignore[union-attr]
    await dialog_manager.done()


window = Window(
    Const("Подтверждаете отмену рассылки?"),
    Row(CANCEL, Button(id="confirm", text=Const("Да"), on_click=on_click)),
    state=CancelMailingSG.confirm,
)
