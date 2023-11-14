from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from inclusive_dance_bot.db.base import Base
from inclusive_dance_bot.db.mixins import TimestampMixin
from inclusive_dance_bot.enums import FeedbackType, MailingStatus, SubmenuType


class User(TimestampMixin, Base):
    __tablename__ = "users"  # type: ignore[assignment]
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
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


class Submenu(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[SubmenuType] = mapped_column(
        ChoiceType(choices=SubmenuType, impl=String(32)), nullable=False
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    button_text: Mapped[str] = mapped_column(String(64), nullable=False)
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


class Mailing(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    status: Mapped[MailingStatus] = mapped_column(
        ChoiceType(choices=MailingStatus, impl=String(16)),
        nullable=False,
        default=MailingStatus.SCHEDULED,
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    content: Mapped[str] = mapped_column(String(3072), nullable=False, default="")

    user_types: Mapped[list["UserType"]] = relationship(
        "UserType", secondary="mailing_user_type"
    )


class MailingUserType(Base):
    mailing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("mailing.id"), primary_key=True
    )
    user_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_type.id"), primary_key=True
    )
