from datetime import datetime

import pytz
from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column


def now_with_tz() -> datetime:
    return datetime.now(tz=pytz.UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz,
        server_default=text("TIMEZONE('utc', now())"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz,
        onupdate=now_with_tz,
        server_default=text("TIMEZONE('utc', now())"),
    )
