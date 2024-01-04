from aiogram import Router

from idb.bot.dialogs.admins.mailings import cancel, create, read

router = Router()
router.include_routers(
    read.dialog,
    cancel.dialog,
    create.dialog,
)
