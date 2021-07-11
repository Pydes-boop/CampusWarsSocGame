__all__ = (
    "now",
    "timestamp",
    "from_timestamp",
)

from time import time
from datetime import datetime, timezone
import pytz
import calendar
from time import gmtime
from time import strftime

START_SUMMER_TERM = 4
END_SUMMER_TERM = 9

tz = pytz.timezone("Europe/Vienna")


def now() -> datetime:
    return datetime.now(tz)


def timestamp() -> int:
    return int(now().timestamp())


def from_timestamp(timestamp_var: int) -> datetime:
    return datetime.fromtimestamp(timestamp_var, tz=tz)


def get_current_time_and_day():
    now_var = datetime.now(tz)
    midnight = now_var.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now_var - midnight).seconds
    result = {"seconds": seconds, "day": now_var.weekday()}
    return result


def get_time_as_seconds(hour, minutes):
    now_var = datetime.now()
    time_needed = now_var.replace(hour=hour, minute=minutes, second=0)
    midnight = now_var.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (time_needed - midnight).seconds
    return seconds


def get_day_as_string(day):
    return calendar.day_name[int(day)]


def get_seconds_as_string(seconds):
    return strftime("%H:%M", gmtime(seconds))


def get_current_term():
    today = datetime.today()
    year = today.year % 100
    letter = ""
    if START_SUMMER_TERM <= today.month <= END_SUMMER_TERM:
        letter = "S"
    else:
        letter = "W"
    return str(year) + letter
