from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import SubmenuDto
from inclusive_dance_bot.enums import SubmenuType
from inclusive_dance_bot.exceptions.base import InclusiveDanceError
from inclusive_dance_bot.logic.storage import Storage
from inclusive_dance_bot.utils import NOT_SET, NotSet


async def create_submenu(
    uow: UnitOfWork,
    storage: Storage,
    type: SubmenuType,
    message: str,
    button_text: str,
    weight: int,
) -> SubmenuDto:
    try:
        submenu = await uow.submenus.create(
            type=type,
            button_text=button_text,
            message=message,
            weight=weight,
        )
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await storage.refresh_submenus()
    return submenu


async def delete_submenu_by_id(
    uow: UnitOfWork, storage: Storage, submenu_id: int
) -> None:
    await uow.submenus.delete_by_id(submenu_id=submenu_id)
    await uow.commit()
    await storage.refresh_submenus()


async def update_submenu_by_id(
    uow: UnitOfWork,
    storage: Storage,
    submenu_id: int,
    weight: int | NotSet = NOT_SET,
    type_: SubmenuType | NotSet = NOT_SET,
    button_text: str | NotSet = NOT_SET,
    message: str | NotSet = NOT_SET,
) -> SubmenuDto:
    data: dict[str, str | int | SubmenuType] = {}
    if not isinstance(weight, NotSet):
        data["weight"] = weight
    if not isinstance(type_, NotSet):
        data["type"] = type_
    if not isinstance(button_text, NotSet):
        data["button_text"] = button_text
    if not isinstance(message, NotSet):
        data["message"] = message
    if not data:
        raise ValueError("Update data is empty!")
    try:
        submenu = await uow.submenus.update_by_id(submenu_id=submenu_id, **data)
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
    await uow.commit()
    await storage.refresh_submenus()
    return submenu
