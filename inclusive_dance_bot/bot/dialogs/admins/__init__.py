from aiogram import Router

from inclusive_dance_bot.bot.dialogs.admins import (
    feedbacks,
    mailings,
    main_menu,
    manage_admins,
    submenu,
    url,
)

dialog_router = Router(name="admin_router")
dialog_router.include_routers(
    feedbacks.router,
    main_menu.dialog,
    submenu.router,
    url.router,
    manage_admins.router,
    mailings.router,
)
