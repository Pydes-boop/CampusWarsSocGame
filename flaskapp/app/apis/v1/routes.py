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
import random

from apis.v1.database.interface import add_room, add_lecture, get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_users_of_lecture, get_full_name_of_current_lecture_in_room
from bson.objectid import ObjectId

from data_handler import live_data, team_state


@v1.app_errorhandler(404)
def error_404(_):
    return make_response(jsonify({'exception': 'Not found!', 'code': 404}), 404)


@api.resource('/roomfinder')
class RoomFinder(Resource):
    @request_requires(headers=['uid', 'team', 'latitude', 'longitude'])
    def post(self):
        lat, lon, = map(float, [request.headers['longitude'], request.headers['latitude']])
        room = find_closest_room(lat, lon, 30)
        name = room['roomName']
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=name)
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=name)
        room['occupancy'] = team_state.get_all_team_scores_in_room(name)
        room['occupier'] = team_state.mw[name].time
        room['multiplier'] = team_state.mw[name].multiplier
        return jsonify(room)

    # todo @Robin insert your stuff instead of my dummy stuff
    def get(self):
        result = []
        r = lambda: random.randint(0, 255)
        j = 1
        for i in get_all_rooms():
            color = '#%02X%02X%02X' % (r(), r(), r())
            item = {
                "location":
                    {"longitude": i["location"]["coordinates"][0],
                     "latitude": i["location"]["coordinates"][1]},
                "roomName": i["roomName"],
                "occupier": {"color": color, "name": "Team" + str(j)},
                "currentLecture": get_full_name_of_current_lecture_in_room(i['_id'])
            }
            j = j + 1
            result.append(item)
        return jsonify(result)


@api.resource('/room-join')
class RoomJoin(Resource):
    def get(self):
        """Just for debug purposes."""
        return jsonify(live_data.room_queue)

    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Users can announce that they are in a room."""
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=request.headers['room'])
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=request.headers['room'])
        return jsonify('ok')


@api.resource('/quiz-request')
class QuizRequest(Resource):
    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Tell us that you would like a quiz."""
        live_data.quiz_queue(request.headers['uid'],
                             request.headers['team'],
                             request.headers['room'])
        return jsonify('ok')


@api.resource('/quiz-refresh')
class QuizRefresh(Resource):
    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Refresh quiz state and maybe or join a game."""
        # I know it is the same as above, but we might
        # have to something different here later
        result = live_data.quiz_queue(request.headers['uid'],
                                      request.headers['team'],
                                      request.headers['room'])
        if result:
            descriptor, game, = result
            return jsonify(
                {
                    'gid': game.game_id,
                    'pid': game.get_player_id(request.headers['uid']),
                    'opp-name': 'It was you all along',  # TODO ask Marina how to get the name
                    'opp-team': game.players[not game.get_player_id(request.headers['uid'])].team,
                    'quiz': game.question,  # TODO is there a way to get just a random quiz
                    'game-ready': descriptor == 'game'
                }
            )
        return jsonify('nothing')


@api.resource('/quiz-answer')
class QuizAnswer(Resource):
    @request_requires(headers=['uid', 'gid', 'pid', 'result'])
    def post(self):
        """Answer the quiz."""
        live_data.game_queue[request.headers['gid']].refresh()
        live_data.game_queue.submit_answer(request.headers['gid'], request.headers['pid'], request.headers['outcome'])
        return jsonify('ok')


@api.resource('/quiz-state')
class QuizState(Resource):
    @request_requires(headers=['uid', 'gid', 'pid'])
    def get(self):  # TODO maybe think about combining this with the request above
        """Ask the server if the other player has answered yet, if yes show result."""
        live_data.game_queue[request.headers['gid']].refresh()
        if live_data.game_queue[request.headers['gid']].all_answered:
            return jsonify(live_data.game_queue['gid'].get_result_for_player(request.headers['pid']))

        return jsonify('not yet answered')


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
