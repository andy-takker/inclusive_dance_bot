from typing import Any

from aiogram_dialog import Data, Dialog, DialogManager

from inclusive_dance_bot.bot.dialogs.admins.url.read import item, items


async def on_process_result(
    start_data: Data, result: Any, manager: DialogManager
) -> None:
    if result:
        manager.dialog_data["url_slug"] = result["url_slug"]


dialog = Dialog(
    items.window,
    item.window,
    on_process_result=on_process_result,
)
