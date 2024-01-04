from aiogram import Router

from idb.bot.dialogs.admins import (
    mailings,
    manage_admins,
    submenu,
    url,
)
from idb.bot.dialogs.admins.feedbacks.router import (
    router as feedbacks_router,
)
from idb.bot.dialogs.admins.main_menu.dialog import (
    dialog as main_menu_dialog,
)

dialog_router = Router(name="admin_router")
dialog_router.include_routers(
    feedbacks_router,
    main_menu_dialog,
    submenu.router,
    url.router,
    manage_admins.router,
    mailings.router,
)
