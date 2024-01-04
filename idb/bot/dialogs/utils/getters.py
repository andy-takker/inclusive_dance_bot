from typing import Any

from aiogram_dialog import DialogManager

from idb.utils.cache import AbstractBotCache


async def get_url_data(
    cache: AbstractBotCache, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {"url": await cache.get_url_by_slug(dialog_manager.start_data["url_slug"])}


async def get_submenu_data(
    cache: AbstractBotCache, dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return {
        "submenu": await cache.get_submenu_by_id(
            dialog_manager.start_data["submenu_id"]
        )
    }
