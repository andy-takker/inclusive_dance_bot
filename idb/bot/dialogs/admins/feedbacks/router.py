from aiogram import Router

from idb.bot.dialogs.admins.feedbacks import read
from idb.bot.dialogs.admins.feedbacks.answer.dialog import (
    dialog as answer_dialog,
)

router = Router()
router.include_routers(
    read.dialog,
    answer_dialog,
)
