#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-20"
__version__ = "0.0.1"

__all__ = ('request_requires', 'check_timed_out_users',)

from flask import request, jsonify
from functools import wraps
from datetime import datetime
import pytz

from typing import Any, Callable


def request_requires(**dec_kwargs) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs) -> Any:
            for section, names in dec_kwargs.items():
                for name in map(lambda x: x.lower(), names):
                    if name not in map(lambda x: x.lower(), getattr(request, section).keys()):
                        raise Exception(f'Request was missing the {section}.{name} entry;')
            return method(*args, **kwargs)
        return wrapper
    return decorator


def check_timed_out_users(timedoutusers) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs) -> Any:
            if 'uid' in request.headers and request.headers['uid'] in timedoutusers:
                time = datetime.fromtimestamp(timedoutusers[request.headers["uid"]].time, tz=pytz.timezone('Europe/Vienna'))
                time_pretty = time.strftime("%A %d-%m-%Y, %H:%M:%S")
                reason = 'lost quiz'
                remaining = (time - datetime.now(tz=pytz.timezone('Europe/Vienna')))
                return jsonify(
                    dict(
                        message=f'You are timed out until {time_pretty} due to: {reason}',
                        timestamp=time,
                        total_duration_in_sec=600,
                        minutes_remaining=int(remaining.total_seconds() // 60),
                        seconds_remaining=int(remaining.total_seconds() % 60),
                        total_seconds_remaining=int(remaining.total_seconds()),
                        time_pretty=time_pretty,
                        reason=reason,
                        timed_out=True
                    ))
            return method(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    pass
