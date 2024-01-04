from idb.db.uow import UnitOfWork
from idb.generals.enums import SubmenuType
from inutils.init_data import write_submenus, write_urls, write_user_types

# async def test_init_data_from_scratch(uow: UnitOfWork) -> None:
#     await write_data(uow=uow, filename=PROJECT_FOLDER / "inutils/init_data.yaml")

#     assert len(await uow.urls.list()) > 0
#     assert len(await uow.submenus.list()) > 0
#     assert len(await uow.user_types.list()) > 0


async def test_write_urls_from_scratch(uow: UnitOfWork) -> None:
    urls = [
        {
            "id": 1,
            "slug": "some_url",
            "value": "https://example.com",
        }
    ]

    await write_urls(uow, urls)
    assert len(await uow.urls.list()) == 1


async def test_write_submenus_from_scratch(uow: UnitOfWork) -> None:
    submenus = [
        {
            "id": 1,
            "type": SubmenuType.CHARITY,
            "button_text": "something",
            "message": "Hello",
            "weight": 1.0,
        }
    ]
    await write_submenus(uow, submenus)
    assert len(await uow.submenus.list()) == 1


async def test_write_user_types_from_scratch(uow: UnitOfWork) -> None:
    user_types = [
        {
            "id": 1,
            "name": "Somebody",
        }
    ]
    await write_user_types(uow, user_types)
    assert len(await uow.user_types.list()) == 1
