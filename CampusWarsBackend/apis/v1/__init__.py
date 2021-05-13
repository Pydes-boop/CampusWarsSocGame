#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('v1', 'api',)

from flask import Blueprint
from flask_restful import Api

v1 = Blueprint('v1', __name__)

api = Api(v1)

if __name__ == '__main__':
    pass
