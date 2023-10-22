from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from inclusive_dance_bot.db.base import Base
from inclusive_dance_bot.db.mixins import TimestampMixin
from inclusive_dance_bot.enums import EntityType, FeedbackType


class User(TimestampMixin, Base):
    __tablename__ = "users"  # type: ignore[assignment]
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    region: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    phone_number: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user_types: Mapped[list["UserType"]] = relationship(
        "UserType", secondary="user_type_user"
    )


class UserType(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True, unique=True
    )


class UserTypeUser(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        primary_key=True,
    )
    user_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_type.id"), primary_key=True
    )


class Entity(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[EntityType] = mapped_column(
        ChoiceType(choices=EntityType, impl=String(32)), nullable=False
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    text: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(String(4000), nullable=False)


class Url(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    value: Mapped[str] = mapped_column(String(2048), nullable=False)


class Feedback(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    type: Mapped[FeedbackType] = mapped_column(
        ChoiceType(choices=FeedbackType, impl=String(32)), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(String(4096), nullable=False)
    is_viewed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    viewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    is_answered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    answered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
