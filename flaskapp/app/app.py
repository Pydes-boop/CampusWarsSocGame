#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('app',)

from apis.v1.routes import v1
from apis.v1 import db

import os
from flask import Flask, request, jsonify
from databaseInterface import application, get_all_rooms, add_room


@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )


@application.route('/room/')
def get_rooms():
    return jsonify(
        status=True,
        data=get_all_rooms()
    )


@application.route('/add_room/')
def add_new_room():
    add_room("Test", 50, 40)
    return jsonify(
        status=True,
        data=get_all_rooms()
    )


@application.route('/room_detection/')
def room_detection():
    add_room("Test", 30, 112)
    return jsonify(
        status=True,
        data=get_all_rooms()
    )


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
