#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-15"
__version__ = "0.0.0"

__all__ = ('error_handler', 'exception_factory',)

from datetime import datetime
from flask import jsonify, request
from functools import wraps
from typing import Any, Dict, Callable


def exception_factory(
        ex_type: str,
        description: str,
        url: str,
        status: int
) -> Dict[str, Any]:
    return dict(
        exception=ex_type,
        description=description,
        time=datetime.now().timestamp(),
        url=url,
        status_code=status
    )


def error_handler(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(*args, **kwargs):
        try: return method(*args, **kwargs)
        except Exception as ex: return jsonify(exception_factory(ex.__class__.__name__, str(ex), request.url, 500)), 500
    return wrapper


if __name__ == '__main__':
    pass
