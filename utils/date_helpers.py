import datetime
from typing import Optional


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now()


def pprint_datetime(dt: datetime.datetime) -> Optional[datetime.datetime]:
    return dt.replace(tzinfo=None).isoformat(sep=" ", timespec="seconds") if dt else dt
