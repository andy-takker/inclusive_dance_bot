from aiogram_dialog import Window

from inclusive_dance_bot.bot.dialogs.admins.states import FeedbackAsnwerSG

window = Window(
    state=FeedbackAsnwerSG.input_message,
)
