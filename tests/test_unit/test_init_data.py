from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.init_data import SUBMENUS, URLS, USER_TYPES, init_data


async def test_init_data_from_scratch(uow: UnitOfWork, session: AsyncSession) -> None:
    await init_data(uow=uow)

    assert len(await uow.urls.get_list()) == len(URLS)
    assert len(await uow.submenus.get_list()) == len(SUBMENUS)
    assert len(await uow.user_types.get_list()) == len(USER_TYPES)
