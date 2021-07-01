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
import json
from apis.v1.database import interface
from apis.v1.database.interface import add_room, add_lecture, get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_users_of_lecture, get_full_name_of_current_lecture_in_room, get_current_team, \
    get_player_name, get_current_quizzes, get_questions_of_quiz
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
        if room is None:
            return jsonify('nothing near you')
        name = room['roomName']
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=name)
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=name)
        return_room = {'occupancy': team_state.get_all_team_scores_in_room(name),
                       'occupier': team_state.get_room_occupier(name),
                       'room_name': name, 'lid': room["_id"], 'multiplier': team_state.mw[name].multiplier,
                       "currentLecture": get_full_name_of_current_lecture_in_room(room["_id"])}
        return jsonify(return_room)

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
                "_id": str(i["_id"]),
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


@api.resource('/live-debug')
class LiveDebug(Resource):
    def get(self):
        return jsonify(live_data.room_queue, live_data.quiz_queue, live_data.game_queue)


@api.resource('/quiz-refresh')
class QuizRefresh(Resource):
    @request_requires(headers=['uid', 'team', 'room', 'lid'])
    def post(self):
        """Refresh quiz state and maybe or join a game."""
        # I know it is the same as above, but we might
        # have to something different here later
        result = live_data.quiz_queue(request.headers['uid'],
                                      request.headers['team'],
                                      request.headers['room'],
                                      request.headers['lid'])
        if result:
            descriptor, game, = result
            return jsonify(
                {
                    'gid': game.game_id,  # game_id: a 24 byte string to identify each game
                    'pid': game.get_player_id(request.headers['uid']),  # player_id: 0 or 1 identifies player in game
                    'opp-name': 'It was you all along',  # name of the opponent TODO ask Marina how to get the name
                    'opp-team': game.players[not game.get_player_id(request.headers['uid'])].team,  # name of the opponent team
                    'quiz': game.question,  # quiz in the already specified format TODO is there a way to get just a random quiz
                    'game-ready': descriptor == 'game'  # unimportant
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
        add_lectures_to_user(request.headers["uid"], json.loads(request.headers["lectures"]))
        return


@api.resource('/mygroup')
class MyGroup(Resource):
    @request_requires(headers=['uid'])
    def get(self):
        return jsonify(get_current_team(request.headers['uid']))


@api.resource('/start')
class Start(Resource):
    @request_requires(headers=['passphrase'])
    def post(self):
        if request.headers['passphrase'] == "YOU ONLY CALL THIS TWICE A YEAR PLS":
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
        lectures= ["Englisch - English through Cinema C1: 20S", "Studentische Vollversammlungen - Informatik: 21S",
                   "Praktikum: Grundlagen der Programmierung (IN0002), Di, Mi: 19W",
                   "Echtzeit-Computergrafik (IN0038): 21S", "Ringvorlesung 'Games Engineering' (IN2368): 21S",
                   "Social Gaming (IN0040): 21S", "Einführung in die Theoretische Informatik (IN0011): 21S",
                   "Einführung in die Informatik 1 (IN0001): 19W", "Audiokommunikation: 21S",
                   "Studentische Vollversammlungen - Informatik: 19W", "Interaktive Visualisierung: 20W"]
        return add_lectures_to_user(3, lectures)


if __name__ == '__main__':
    pass
