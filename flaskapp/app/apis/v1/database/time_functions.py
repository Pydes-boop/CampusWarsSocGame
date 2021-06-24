__all__ = ()

from time import time
from datetime import datetime

START_SUMMER_TERM = 4
END_SUMMER_TERM = 9


def get_current_time_in_millis():
    return round(time.time() * 1000)


def get_current_term():
    today = datetime.date.today()
    year = today.year % 100
    letter = ""
    if START_SUMMER_TERM <= today.month <= END_SUMMER_TERM:
        letter = "S"
    else:
        letter = "W"
    return letter + str(year)
