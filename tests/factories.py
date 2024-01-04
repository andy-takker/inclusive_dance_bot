from typing import TypedDict

from polyfactory import Use
from polyfactory.factories import TypedDictFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.value_generators.constrained_strings import (
    handle_constrained_string_or_bytes,
)

from idb.db.models import Feedback, Submenu, Url, User, UserType
from idb.generals.enums import SubmenuType


def _phone_number():
    return handle_constrained_string_or_bytes(
        random=SQLAlchemyFactory.__random__,
        t_type=str,
        min_length=8,
        max_length=16,
    )


class Profile(TypedDict):
    name: str
    region: str
    phone_number: str


class ProfileFactory(TypedDictFactory[Profile]):
    __model__ = Profile

    phone_number = _phone_number


class UserFactory(SQLAlchemyFactory[User]):
    __model__ = User
    __set_foreign_keys__ = False
    __set_relationships__ = True

    profile = ProfileFactory


class UserTypeFactory(SQLAlchemyFactory[UserType]):
    __model__ = UserType
    __set_foreign_keys__ = False
    __set_relationships__ = True


class SubmenuFactory(SQLAlchemyFactory[Submenu]):
    __model__ = Submenu
    __set_foreign_keys__ = False
    __set_relationships__ = True

    type = Use(SQLAlchemyFactory.__random__.choice, list(SubmenuType))


class UrlFactory(SQLAlchemyFactory[Url]):
    __model__ = Url
    __set_foreign_keys__ = False
    __set_relationships__ = True


class FeedbackFactory(SQLAlchemyFactory[Feedback]):
    __model__ = Feedback
    __set_foreign_keys__ = False
    __set_relationships__ = True


FACTORIES: tuple[SQLAlchemyFactory, ...] = (
    UserFactory,
    UserTypeFactory,
    SubmenuFactory,
    UrlFactory,
    FeedbackFactory,
)
