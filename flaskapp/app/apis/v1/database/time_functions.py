__all__ = ()

from time import time
from datetime import datetime, timezone
import pytz
import calendar
from time import gmtime
from time import strftime

START_SUMMER_TERM = 4
END_SUMMER_TERM = 9


def get_current_time_and_day():
    now = datetime.now(pytz.timezone('Europe/Vienna'))
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    result = (seconds, now.weekday())
    return result


def get_time_as_seconds(hour, minutes):
    now = datetime.now()
    time_needed = now.replace(hour=hour, minute=minutes, second=0)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (time_needed - midnight).seconds
    return seconds


def get_day_as_string(day):
    return calendar.day_name[day]


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
    return letter + str(year)
