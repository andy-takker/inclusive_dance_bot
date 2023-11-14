from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins.manage_admins import add, delete, read

router = Router()
router.include_routers(
    add.dialog,
    delete.dialog,
    read.dialog,
)
