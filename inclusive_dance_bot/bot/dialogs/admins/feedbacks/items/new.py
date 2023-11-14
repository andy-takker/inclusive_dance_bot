from aiogram_dialog import Window

from inclusive_dance_bot.bot.dialogs.admins.states import FeedbackItemsSG

window = Window(
    state=FeedbackItemsSG.new,
)
