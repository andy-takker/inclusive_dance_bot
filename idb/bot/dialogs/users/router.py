from aiogram import Router

from idb.bot.dialogs.users import (
    feedback,
    main_menu,
    registration,
    submenu,
)

dialog_router = Router(name="user_router")
dialog_router.include_routers(
    feedback.dialog,
    main_menu.dialog,
    registration.dialog,
    submenu.dialog,
)
