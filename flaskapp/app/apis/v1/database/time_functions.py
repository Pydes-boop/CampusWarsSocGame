__all__ = ()

from time import time
from datetime import datetime

START_SUMMER_TERM = 4
END_SUMMER_TERM = 9


def get_current_time_and_day():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    result = (seconds, now.weekday())
    return result


def get_current_term():
    today = datetime.date.today()
    year = today.year % 100
    letter = ""
    if START_SUMMER_TERM <= today.month <= END_SUMMER_TERM:
        letter = "S"
    else:
        letter = "W"
    return letter + str(year)
