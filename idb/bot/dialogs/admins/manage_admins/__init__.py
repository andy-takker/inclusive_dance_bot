from aiogram import Router

from idb.bot.dialogs.admins.manage_admins import add, delete, read

router = Router()
router.include_routers(
    add.dialog,
    delete.dialog,
    read.dialog,
)
