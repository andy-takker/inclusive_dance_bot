import re
from datetime import datetime

import pytz
from sqlalchemy import DateTime, MetaData, text
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)  # type:ignore[arg-type]


@as_declarative(metadata=metadata)
class Base:
    metadata: MetaData

    @declared_attr  # type:ignore[arg-type]
    def __tablename__(cls) -> str:
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()


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
