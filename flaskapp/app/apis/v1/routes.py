#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('v1',)

from flask import jsonify, request, make_response
from flask_restful import Resource
from apis.v1 import v1, api
import groupCreation
from apis.v1.decorators import request_requires

from apis.v1.database.interface import add_room, add_lecture, get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_users_of_lecture
from bson.objectid import ObjectId


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


@api.resource('/roomfinder')
class RoomFinder(Resource):
    @request_requires(headers=['latitude', 'longitude'])
    def post(self):
        return jsonify(find_closest_room(request.headers["longitude"], request.headers["latitude"], 30))

    def get(self):
        result = []
        for i in get_all_rooms():
            item = {
                "location":
                    {"longitude": i["location"]["coordinates"][0],
                     "latitude": i["location"]["coordinates"][1]},
                "roomName": i["roomName"]
            }
            result.append(item)
        return jsonify(result)


@api.resource('/echo')
class Echo(Resource):
    def get(self):
        return "Hallo Echo!", 200


@api.resource('/lectures')
class Lectures(Resource):
    def post(self):
        set_user_lectures(request.headers["uid"], request.headers["lectures"])
        return


@api.resource('/start')
class Start(Resource):
    def post(self):
        groupCreation.create_groups()
        return "ok", 200


@api.resource('/question')
class Question(Resource):
    def post(self):
        # todo: get questions from body and process to database
        add_question_to_quiz(1, 2, 3, 4)
        return "ok", 200


@api.resource('/register')
class Register(Resource):
    def post(self):
        add_user(request.headers["uid"], request.headers["name"])
        return "ok", 200


@api.resource('/marina')
class Test(Resource):
    def get(self):
        add_user(1, "marina", [ObjectId("60d5dfe18343a7a71befce4b")])
        return get_users_of_lecture("60d5dfe18343a7a71befce4b")


if __name__ == '__main__':
    pass
