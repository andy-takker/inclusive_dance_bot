from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from git import Sequence

from inclusive_dance_bot.db.models import Mailing
from inclusive_dance_bot.enums import FeedbackType, MailingStatus, SubmenuType

if TYPE_CHECKING:
    from inclusive_dance_bot.db.models import (
        Feedback,
        Mailing,
        Submenu,
        Url,
        User,
        UserType,
    )


@dataclass(frozen=True, slots=True)
class UserDto:
    id: int
    name: str
    username: str
    region: str
    phone_number: str
    is_admin: bool

    @classmethod
    def from_orm(cls, obj: User) -> UserDto:
        return cls(
            id=obj.id,
            name=obj.name,
            username=obj.username,
            region=obj.name,
            phone_number=obj.phone_number,
            is_admin=obj.is_admin,
        )


ANONYMOUS_USER = UserDto(
    id=0,
    name="Anonymous",
    region="Earth",
    phone_number="",
    is_admin=False,
    username="anonymous",
)


@dataclass(frozen=True, slots=True)
class UserTypeDto:
    id: int
    name: str

    @classmethod
    def from_orm(cls, obj: UserType) -> UserTypeDto:
        return cls(id=obj.id, name=obj.name)


@dataclass(frozen=True, slots=True)
class SubmenuDto:
    id: int
    type: SubmenuType
    weight: int
    button_text: str
    message: str

    @classmethod
    def from_orm(cls, obj: Submenu) -> SubmenuDto:
        return cls(
            id=obj.id,
            type=obj.type,
            weight=obj.weight,
            button_text=obj.button_text,
            message=obj.message,
        )


@dataclass(frozen=True, slots=True)
class UrlDto:
    id: int
    slug: str
    value: str

    @classmethod
    def from_orm(cls, obj: Url) -> UrlDto:
        return cls(id=obj.id, slug=obj.slug, value=obj.value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
class MailingDto:
    created_at: datetime
    updated_at: datetime
    id: int
    scheduled_at: datetime | None
    sent_at: datetime | None
    cancelled_at: datetime | None
    status: MailingStatus
    title: str
    content: str
    user_types: Sequence[UserTypeDto]

    @classmethod
    def from_orm(cls, obj: Mailing) -> MailingDto:
        return cls(
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            id=obj.id,
            scheduled_at=obj.scheduled_at,
            cancelled_at=obj.cancelled_at,
            status=obj.status,
            title=obj.title,
            content=obj.content,
            user_types=tuple(UserTypeDto.from_orm(ut) for ut in obj.user_types),
            sent_at=obj.sent_at,
        )
