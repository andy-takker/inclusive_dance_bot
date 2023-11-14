from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import AdminMainMenuSG, CreateUrlSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.logic.url import create_url


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await create_url(
        uow=uow,
        storage=storage,
        slug=dialog_manager.dialog_data["slug"],
        value=dialog_manager.dialog_data["value"],
    )
    dialog_manager.show_mode = ShowMode.SEND
    await c.bot.send_message(c.from_user.id, text="Ссылка была сохранена")  # type: ignore[union-attr]
    await dialog_manager.start(state=AdminMainMenuSG.menu, mode=StartMode.RESET_STACK)


window = Window(
    Format("Слаг: {dialog_data[slug]}\nЗначение: {dialog_data[value]}"),
    Row(
        BACK,
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=CreateUrlSG.confirm,
)
