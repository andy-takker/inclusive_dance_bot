from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins.mailings import cancel, create, read

router = Router()
router.include_routers(
    read.dialog,
    cancel.dialog,
    create.dialog,
)
