from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins import main_menu, submenu, url


def register_admin_dialogs() -> Router:
    dialog_router = Router(name="admin_router")
    dialog_router.include_router(main_menu.dialog)
    dialog_router.include_router(submenu.router)
    dialog_router.include_router(url.router)
    return dialog_router
