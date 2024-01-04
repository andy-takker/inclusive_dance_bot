from collections.abc import Iterable

from idb.db.uow import UnitOfWork
from idb.exceptions.base import InclusiveDanceError


async def save_profile_user(
    uow: UnitOfWork,
    user_id: int,
    name: str,
    region: str,
    phone_number: str,
    user_type_ids: Iterable[int],
) -> None:
    """Сохраняет профиль нового пользователя"""
    try:
        await uow.users.update_by_id(
            user_id=user_id,
            profile={
                "name": name,
                "region": region,
                "phone_number": phone_number,
            },
        )
        for user_type_id in user_type_ids:
            await uow.user_type_users.create(
                user_id=user_id,
                user_type_id=user_type_id,
            )
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def add_user_to_admins(uow: UnitOfWork, username: str) -> None:
    try:
        await uow.users.add_to_admins(username=username)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e


async def delete_from_admins(uow: UnitOfWork, user_id: int) -> None:
    try:
        await uow.users.delete_from_admins(user_id=user_id)
        await uow.commit()
    except InclusiveDanceError as e:
        await uow.rollback()
        raise e
