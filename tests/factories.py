from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.value_generators.constrained_strings import (
    handle_constrained_string_or_bytes,
)

from inclusive_dance_bot.db.models import Entity, Feedback, Url, User, UserType
from inclusive_dance_bot.enums import EntityType


class UserFactory(SQLAlchemyFactory[User]):
    __model__ = User
    __set_foreign_keys__ = False
    __set_relationships__ = True

    phone_number = lambda: handle_constrained_string_or_bytes(
        random=SQLAlchemyFactory.__random__, t_type=str, min_length=8, max_length=16
    )


class UserTypeFactory(SQLAlchemyFactory[UserType]):
    __model__ = UserType
    __set_foreign_keys__ = False
    __set_relationships__ = True


class EntityFactory(SQLAlchemyFactory[Entity]):
    __model__ = Entity
    __set_foreign_keys__ = False
    __set_relationships__ = True

    type = Use(SQLAlchemyFactory.__random__.choice, list(EntityType))


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
    EntityFactory,
    UrlFactory,
    FeedbackFactory,
)
