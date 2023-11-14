from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Next, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from inclusive_dance_bot.bot.dialogs.admins.states import CreateMailingSG
from inclusive_dance_bot.bot.dialogs.utils.buttons import BACK

window = Window(
    Const("Когда отправить?"),
    Row(
        Next(text=Const("По расписанию")),
        SwitchTo(
            text=Const("Немедленно"), id="send_mailing", state=CreateMailingSG.confirm
        ),
    ),
    BACK,
    state=CreateMailingSG.is_immediately,
)
