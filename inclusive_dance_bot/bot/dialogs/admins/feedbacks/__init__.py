from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins.feedbacks import answer, items

router = Router()
router.include_routers(
    items.dialog,
    answer.dialog,
)
