from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins.submenu import create, delete, read, update

router = Router()
router.include_routers(
    create.dialog,
    read.dialog,
    update.dialog,
    delete.dialog,
)
