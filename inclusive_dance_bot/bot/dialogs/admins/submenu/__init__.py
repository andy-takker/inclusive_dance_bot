from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins.submenu import create, delete, read, update

router = Router()
# router.include_router(create.dialog)
router.include_router(read.dialog)
# router.include_router(update.dialog)
# router.include_router(delete.dialog)
