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
from apis.v1.decorators import request_requires, check_timed_out_users
import json
import threading
from apis.v1.database import interface
from apis.v1.database.interface import get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_full_name_of_current_lecture_in_room, get_player_name, get_time_table_of_room, \
    get_escaped_by_db, get_current_team_with_member_names, get_colour_of_team
from contextlib import suppress
from apis.v1.database.data_handler import live_data, team_state
import ftfy

ROOMFINDER_TESTING: int = 50


@v1.app_errorhandler(404)
def error_404(_):
    return make_response(jsonify({'exception': 'Not found!', 'code': 404}), 404)


@api.resource('/roomfinder')
class RoomFinder(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'latitude', 'longitude'])
    def post(self):
        lat, lon, = map(float, [request.headers['longitude'], request.headers['latitude']])
        room = find_closest_room(lat, lon, ROOMFINDER_TESTING)
        if room is None:
            return jsonify({"message": 'nothing near you'})
        name = room['roomName']
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=name)
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=name)
        return_room = {"message": "closest room to you:",
                       'occupancy': team_state.get_all_team_occupancy_in_room(name),
                       'occupier': team_state.get_room_occupier(name),
                       'room_name': name, 'lid': str(room["_id"]),
                       'multiplier': team_state.mw[name].multiplier,
                       "currentLecture": get_full_name_of_current_lecture_in_room(str(room["_id"]))}
        return jsonify(return_room)

    def get(self):
        result = []
        for i in get_all_rooms():
            occupier = team_state.get_room_occupier(i['roomName']) or 'Nobody'
            if occupier:
                color = get_colour_of_team(occupier)
            else:
                color = '#212121'
            timetable = get_time_table_of_room(i["_id"])
            item = {
                "location":
                    {"longitude": i["location"]["coordinates"][0],
                     "latitude": i["location"]["coordinates"][1]},
                "roomName": i["roomName"],
                "_id": str(i["_id"]),
                "occupier": {"color": color, "name": occupier},
                "currentLecture": get_full_name_of_current_lecture_in_room(i['_id']),
                "timetable": timetable
            }
            result.append(item)
        return jsonify(result)


@api.resource('/room-join')
class RoomJoin(Resource):
    def get(self):
        """Just for debug purposes."""
        return jsonify(live_data.room_queue)

    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Users can announce that they are in a room."""
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=request.headers['room'])
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=request.headers['room'])
        return jsonify({'joined': True})


@api.resource('/quiz-request')
class QuizRequest(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Tell us that you would like a quiz."""
        if request.headers['uid'] not in live_data.room_queue:
            return jsonify({'quiz-request': False, 'reason': 'not in a room'})
        live_data.quiz_queue(request.headers['uid'],
                             request.headers['team'],
                             request.headers['room'])
        return jsonify({'quiz-request': True})


@api.resource('/live-debug')
class LiveDebug(Resource):
    def get(self):
        return jsonify(live_data.room_queue,
                       live_data.quiz_queue,
                       dict([(key, item.json) for key, item in live_data.game_queue.items()]),
                       live_data.timedout_users
                       )


@api.resource('/quiz-refresh')
class QuizRefresh(Resource):
    @check_timed_out_users(live_data.timedout_users)
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
                    'opp-name': get_player_name(game.players[not game.get_player_id(request.headers['uid'])].uid),
                    'opp-team': game.players[not game.get_player_id(request.headers['uid'])].team,
                    'name': game.name,  # name of the opponent team
                    'quiz': game.question,  # quiz in the already specified format
                    'game-ready': descriptor == 'game'  # unimportant
                }
            )
        return jsonify({'nothing': True})


@api.resource('/quiz-answer')
class QuizAnswer(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid', 'result', 'outcome'])
    def post(self):
        """Answer the quiz."""
        live_data.game_queue[request.headers['gid']].refresh()
        live_data.game_queue.submit_answer(request.headers['gid'], int(request.headers['pid']),
                                           int(request.headers['outcome']))
        return jsonify({'quiz-answer': True})


@api.resource('/quiz-state')
class QuizState(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid'])
    def get(self):
        """Ask the server if the other player has answered yet, if yes show result."""
        live_data.game_queue[request.headers['gid']].refresh()
        if live_data.game_queue[request.headers['gid']].all_answered:
            result = live_data.game_queue[request.headers['gid']].get_result_for_player(int(request.headers['pid']))
            live_data.game_queue[request.headers['gid']].set_finished(int(request.headers['pid']))
            if live_data.game_queue[request.headers['gid']].is_finished:
                with suppress(ValueError): del live_data.game_queue[request.headers['gid']]
            if result == 'LOST': live_data.timedout_users(request.headers['uid'])
            return jsonify(result)

        return jsonify({'not yet answered': True})


@api.resource('/echo')
class Echo(Resource):
    def get(self):
        return "Hallo Echo!", 200


@api.resource('/lectures')
class Lectures(Resource):
    def post(self):
        lectures = json.loads(request.headers["lectures"])
        lecturesList = []
        for lec in lectures:
            lecturesList.append(
                ftfy.fix_text(
                    get_escaped_by_db(lec.encode(request.headers["encodingformat"]).decode('utf-8'))))
        if groupCreation.threshold < interface.get_number_of_players():
            group_creation = threading.Thread(target=groupCreation.alternative_calculation)
            group_creation.start()
            groupCreation.threshold = (groupCreation.threshold * 1.6)
        return add_lectures_to_user(request.headers["uid"], lecturesList)


@api.resource('/mygroup')
class MyGroup(Resource):
    @request_requires(headers=['uid'])
    def get(self):
        return jsonify(get_current_team_with_member_names(request.headers['uid']))


@api.resource('/start')
class Start(Resource):
    @request_requires(headers=['passphrase', 'variant'])
    def post(self):
        if request.headers['passphrase'] == "YOU ONLY CALL THIS TWICE A YEAR PLS":
            if request.headers['variant'] == "pulp":
                group_creation = threading.Thread(target=groupCreation.wedding_seating)
            elif request.headers['variant'] == "metis":
                group_creation = threading.Thread(target=groupCreation.metis_calulation)
            elif request.headers['variant'] == "greedy":
                group_creation = threading.Thread(target=groupCreation.greedy_random)
            else:
                group_creation = threading.Thread(target=groupCreation.alternative_calculation)

            group_creation.start()
            return jsonify({'message': "Started group creation"})
        return jsonify({'message':'You are not allowed to restart'})


@api.resource('/question')
class Question(Resource):
    @request_requires(headers=['question', 'right_answer', 'wrong_answers', 'quiz_id'])
    def post(self):
        status = add_question_to_quiz(request.headers['question'], request.headers['right_answer'],
                                      request.headers['wrong_answers'], request.headers['quiz_id'])
        return jsonify({'success': status})


@api.resource('/register')
class Register(Resource):
    def post(self):
        status = add_user(request.headers["uid"], request.headers["name"])
        return jsonify({'success': status})


@api.resource('/timetable')
class TimeTable(Resource):
    @request_requires(headers=['room_id'])
    def post(self):
        return get_time_table_of_room(request.headers['room_id'])


@api.resource('/marina')
class Test(Resource):
    def get(self):
        return jsonify(groupCreation.alternative_calculation())


@api.resource('/felix')
class AlsoTest(Resource):
    def get(self):
        return jsonify(interface.get_all_teams())


if __name__ == '__main__':
    pass
