from aiogram import Router

from src.dialogs.admins.main_menu import AdminMainMenuDialog


def register_admin_dialogs() -> Router:
    dialog_router = Router(name="admin_router")
    dialog_router.include_router(AdminMainMenuDialog())

    return dialog_router
