#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('v1',)

from flask import jsonify, request, make_response
from flask_restful import Resource
from apis.v1 import v1, api
import databaseInterface
import groupCreation
from apis.v1.decorators import request_requires


@v1.app_errorhandler(404)
def error_404(_):
    return make_response(jsonify({'exception': 'Not found!', 'code': 404}), 404)


@api.resource('/lecturehalls/<int:number>')
class LectureHalls(Resource):
    def get(self, number):
        # TODO replace with actual lookup
        return jsonify(
            [
                number,
                {'name': 'MW-1', 'location': [50, 10]},
                {'name': 'MW-2', 'location': [51, 9]},
                {'name': 'MI-1', 'location': [50, 9]},
                {'name': 'MI-2', 'location': [51, 10]}
            ]
        )


@api.resource('/quiz')
class Quiz(Resource):
    @staticmethod
    def get():
        # TODO replace with actual lookup
        return jsonify(
            [
                {'name': 'MW-1', 'location': [50, 10]},
                {'name': 'MW-2', 'location': [51, 9]},
                {'name': 'MI-1', 'location': [50, 9]},
                {'name': 'MI-2', 'location': [51, 10]}
            ]
        )


@api.resource('/roomdetection')
class RoomDetection(Resource):
    @request_requires(headers=['latitude', 'longitude'])
    def post(self):
        return jsonify(databaseInterface.room_detection(request.headers["latitude"], request.headers["longitude"],
                                                        request.headers["uid"]))

    def get(self):
        return jsonify(databaseInterface.get_all_rooms())


@api.resource('/echo')
class Echo(Resource):
    def get(self):
        return "Hallo Echo!", 200


@api.resource('/groups')
class Groups(Resource):
    def get(self):
        # todo: frontend pls define what to return
        return jsonify(databaseInterface.get_all_groups())

    def post(self):
        # todo: get user selected groups from body not header
        return jsonify(databaseInterface.set_user_groups(request.headers["user"], request.headers["groups"]))


@api.resource('/start')
class Start(Resource):
    def post(self):
        groupCreation.create_groups()
        return "ok", 200


@api.resource('/question')
class Question(Resource):
    def post(self):
        # todo: get questions from body and process to database
        databaseInterface.add_question(1, 2, 3)
        return "ok", 200


@api.resource('/register')
class Register(Resource):
    def post(self):
        databaseInterface.register(request.headers["user"])
        return "ok", 200
if __name__ == '__main__':
    pass
