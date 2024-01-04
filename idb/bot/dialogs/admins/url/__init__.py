from aiogram import Router

from idb.bot.dialogs.admins.url import create, delete, read, update

router = Router()
router.include_routers(
    create.dialog,
    read.dialog,
    update.dialog,
    delete.dialog,
)
