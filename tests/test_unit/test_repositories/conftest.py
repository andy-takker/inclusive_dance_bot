import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from idb.db.repositories.feedback import FeedbackRepository
from idb.db.repositories.submenu import SubmenuRepository
from idb.db.repositories.url import UrlRepository
from idb.db.repositories.user import UserRepository
from idb.db.repositories.user_type import UserTypeRepository
from idb.db.repositories.user_type_user import UserTypeUserRepository


@pytest.fixture
def submenu_repo(session: AsyncSession) -> SubmenuRepository:
    return SubmenuRepository(session=session)


@pytest.fixture
def url_repo(session: AsyncSession) -> UrlRepository:
    return UrlRepository(session=session)


@pytest.fixture
def user_type_repo(session: AsyncSession) -> UserTypeRepository:
    return UserTypeRepository(session=session)


@pytest.fixture
def user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session=session)


@pytest.fixture
def user_type_user_repo(session: AsyncSession) -> UserTypeUserRepository:
    return UserTypeUserRepository(session=session)


@pytest.fixture
def feedback_repo(session: AsyncSession) -> FeedbackRepository:
    return FeedbackRepository(session=session)
