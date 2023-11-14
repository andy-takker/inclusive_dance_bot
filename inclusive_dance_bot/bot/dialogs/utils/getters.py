from typing import Any

from aiogram_dialog import DialogManager

from inclusive_dance_bot.logic.storage import Storage


async def get_url_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {"url": await storage.get_url_by_slug(dialog_manager.start_data["url_slug"])}


async def get_submenu_data(
    storage: Storage, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "submenu": await storage.get_submenu_by_id(
            dialog_manager.start_data["submenu_id"]
        )
    }
