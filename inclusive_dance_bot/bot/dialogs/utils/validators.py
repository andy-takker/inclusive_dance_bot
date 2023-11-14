from collections.abc import Callable
from datetime import date, datetime, time


def validate_length(length: int) -> Callable[[str], str]:
    def validator(value: str) -> str:
        if len(value) > length:
            raise ValueError
        return value

    return validator


def validate_date(date_format: str = "%d.%m.%Y") -> Callable[[str], date]:
    def validator(value: str) -> date:
        return datetime.strptime(value, date_format).date()

    return validator


def validate_time(time_format: str = "%H:%M") -> Callable[[str], time]:
    def validator(value: str) -> time:
        return datetime.strptime(value, time_format).time()

    return validator
