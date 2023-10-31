from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Button, Row
from aiogram_dialog.widgets.text import Const, Format

from inclusive_dance_bot.bot.dialogs.admins.states import AdminMainMenuSG, CreateUrlSG
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.save_data import save_new_url
from inclusive_dance_bot.services.storage import Storage


async def on_click(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    storage: Storage = dialog_manager.middleware_data["storage"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    await save_new_url(
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
        Back(text=Const("Назад")),
        Button(text=Const("Сохранить"), id="save", on_click=on_click),
    ),
    state=CreateUrlSG.confirm,
)
