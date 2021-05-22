#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('v1', 'api', 'db',)

from flask import Blueprint
from flask_restful import Api
from flask_mongoengine import MongoEngine
from apis.v1.errorhandler import error_handler

v1 = Blueprint('v1', __name__)

api = Api(v1)

api.decorators.append(error_handler)

db = MongoEngine()

if __name__ == '__main__':
    pass
