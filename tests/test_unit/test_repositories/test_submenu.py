import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.models import Submenu as SubmenuDb
from idb.db.repositories.submenu import SubmenuRepository
from idb.exceptions import (
    SubmenuAlreadyExistsError,
    SubmenuNotFoundError,
)
from idb.generals.enums import SubmenuType
from idb.generals.models.submenu import Submenu
from tests.factories import SubmenuFactory


async def test_create(submenu_repo: SubmenuRepository, session: AsyncSession) -> None:
    submenu = await submenu_repo.create(
        type=SubmenuType.INFORMATION,
        button_text="some submenu",
        message="Very long message message",
    )
    await session.commit()
    saved_submenu = await session.get(SubmenuDb, submenu.id)
    assert submenu == Submenu.model_validate(saved_submenu)


async def test_invalid_double_create(
    submenu_repo: SubmenuRepository, session: AsyncSession
) -> None:
    await submenu_repo.create(
        id=1,
        type=SubmenuType.INFORMATION,
        button_text="some submenu",
        message="Very long message message",
    )
    await session.commit()
    with pytest.raises(SubmenuAlreadyExistsError):
        await submenu_repo.create(
            id=1,
            type=SubmenuType.INFORMATION,
            button_text="some submenu",
            message="Very long message message",
        )


async def test_get_by_id(submenu_repo: SubmenuRepository) -> None:
    submenu = await SubmenuFactory.create_async()
    loaded_submenu = await submenu_repo.get_by_id(submenu.id)
    assert Submenu.model_validate(submenu) == loaded_submenu


async def test_not_found_by_id(submenu_repo: SubmenuRepository) -> None:
    with pytest.raises(SubmenuNotFoundError):
        await submenu_repo.get_by_id(-1)


async def test_get_list_emtpy(submenu_repo: SubmenuRepository) -> None:
    empty = await submenu_repo.list()
    assert empty == tuple()


async def test_get_list(submenu_repo: SubmenuRepository) -> None:
    submenus = await SubmenuFactory.create_batch_async(size=5)
    submenus.sort(key=lambda x: (-x.weight, x.id))
    loaded_submenus = await submenu_repo.list()
    assert loaded_submenus == tuple(Submenu.model_validate(s) for s in submenus)


async def test_get_list_order_by_weight(submenu_repo: SubmenuRepository) -> None:
    third = await SubmenuFactory.create_async(weight=1)
    first = await SubmenuFactory.create_async(weight=100)
    second = await SubmenuFactory.create_async(weight=30)

    loaded_submenus = await submenu_repo.list()
    assert loaded_submenus == tuple(
        Submenu.model_validate(e) for e in (first, second, third)
    )


async def test_get_list_by_correct_type(submenu_repo: SubmenuRepository) -> None:
    target_type = await SubmenuFactory.create_async(type=SubmenuType.CHARITY)

    charities = await submenu_repo.get_list_by_type(SubmenuType.CHARITY)

    assert charities == [Submenu.model_validate(target_type)]


async def test_get_list_by_incorrect_type(submenu_repo: SubmenuRepository) -> None:
    await SubmenuFactory.create_async(type=SubmenuType.EDUCATION)

    charities = await submenu_repo.get_list_by_type(SubmenuType.CHARITY)
    assert charities == list()
