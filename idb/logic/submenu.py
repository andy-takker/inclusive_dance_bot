from idb.db.uow import UnitOfWork
from idb.exceptions.base import InclusiveDanceError
from idb.generals.enums import SubmenuType
from idb.generals.models.submenu import Submenu
from idb.utils.cache import AbstractBotCache
from idb.utils.urls import NOT_SET, NotSet


async def create_submenu(
    uow: UnitOfWork,
    cache: AbstractBotCache,
    type: SubmenuType,
    message: str,
    button_text: str,
    weight: int,
) -> Submenu:
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
    await cache.update_submenu(id_=submenu.id, submenu=submenu)
    return submenu


async def delete_submenu_by_id(
    uow: UnitOfWork, cache: AbstractBotCache, submenu_id: int
) -> None:
    await uow.submenus.delete_by_id(submenu_id=submenu_id)
    await uow.commit()
    await cache.update_submenu(id_=submenu_id, submenu=None)


async def update_submenu_by_id(
    uow: UnitOfWork,
    cache: AbstractBotCache,
    submenu_id: int,
    weight: int | NotSet = NOT_SET,
    type_: SubmenuType | NotSet = NOT_SET,
    button_text: str | NotSet = NOT_SET,
    message: str | NotSet = NOT_SET,
) -> Submenu:
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
    await cache.update_submenu(id_=submenu.id, submenu=submenu)
    return submenu
