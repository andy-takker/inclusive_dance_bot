import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from inclusive_dance_bot.db.repositories.entity import EntityRepository
from inclusive_dance_bot.db.repositories.feedback import FeedbackRepository
from inclusive_dance_bot.db.repositories.url import UrlRepository
from inclusive_dance_bot.db.repositories.user import UserRepository
from inclusive_dance_bot.db.repositories.user_type import UserTypeRepository
from inclusive_dance_bot.db.repositories.user_type_user import UserTypeUserRepository


@pytest.fixture
def entity_repo(session: AsyncSession) -> EntityRepository:
    return EntityRepository(session=session)


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
