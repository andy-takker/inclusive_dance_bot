from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from inclusive_dance_bot.enums import EntityType, FeedbackType

if TYPE_CHECKING:
    from inclusive_dance_bot.db.models import Entity, Feedback, Url, User, UserType


@dataclass(frozen=True)
class UserDto:
    id: int
    name: str
    region: str
    phone_number: str
    is_admin: bool

    @classmethod
    def from_orm(cls, obj: User) -> UserDto:
        return cls(
            id=obj.id,
            name=obj.name,
            region=obj.name,
            phone_number=obj.phone_number,
            is_admin=obj.is_admin,
        )


@dataclass(frozen=True)
class UserTypeDto:
    id: int
    name: str

    @classmethod
    def from_orm(cls, obj: UserType) -> UserTypeDto:
        return cls(id=obj.id, name=obj.name)


@dataclass(frozen=True)
class EntityDto:
    id: int
    type: EntityType
    weight: int
    text: str
    message: str

    @classmethod
    def from_orm(cls, obj: Entity) -> EntityDto:
        return cls(
            id=obj.id,
            type=obj.type,
            weight=obj.weight,
            text=obj.text,
            message=obj.message,
        )


@dataclass(frozen=True)
class UrlDto:
    id: int
    slug: str
    value: str

    @classmethod
    def from_orm(cls, obj: Url) -> UrlDto:
        return cls(id=obj.id, slug=obj.slug, value=obj.value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class FeedbackDto:
    id: int
    user_id: int
    type: FeedbackType
    title: str
    text: str
    is_viewed: bool
    viewed_at: datetime | None
    is_answered: bool
    answered_at: datetime | None

    @classmethod
    def from_orm(cls, obj: Feedback) -> FeedbackDto:
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            type=obj.type,
            title=obj.title,
            text=obj.text,
            is_viewed=obj.is_viewed,
            viewed_at=obj.viewed_at,
            is_answered=obj.is_answered,
            answered_at=obj.answered_at,
        )
