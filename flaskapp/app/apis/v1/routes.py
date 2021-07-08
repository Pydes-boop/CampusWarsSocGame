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
from operator import attrgetter
from apis.v1.database import interface
from apis.v1.database.interface import get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_full_name_of_current_lecture_in_room, get_player_name, get_time_table_of_room, \
    get_escaped_by_db, get_current_team_with_member_names, get_colour_of_team
from contextlib import suppress
from apis.v1.database.live_data import LiveData
import ftfy

live_data = LiveData()

ROOMFINDER_DISTANCE: int = 50


@v1.app_errorhandler(404)
def error_404(_):
    return make_response(jsonify({'exception': 'Not found!', 'code': 404}), 404)


@api.resource('/roomfinder')
class RoomFinder(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'latitude', 'longitude'])
    def post(self):
        lat, lon, = map(float, [request.headers['longitude'], request.headers['latitude']])
        room = find_closest_room(lat, lon, ROOMFINDER_DISTANCE)
        if room is None:
            return jsonify({"message": 'nothing near you'})
        room_name = room['roomName']
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=room_name)
        occupier = live_data.room_queue.get_each_rooms_occupiers()[room_name]
        occupier_team = occupier.team
        occupier_multiplier = occupier.multiplier
        team_occupancy = live_data.room_queue.get_each_rooms_occupancies()[room_name]
        with suppress(KeyError): team_occupancy[occupier_team] *= occupier_multiplier
        return_room = {"message": "closest room to you:",
                       'occupancy': team_occupancy,
                       'occupier': occupier_team,
                       'room_name': room_name, 'lid': str(room["_id"]),
                       'multiplier': occupier_multiplier,
                       "currentLecture": get_full_name_of_current_lecture_in_room(str(room["_id"]))}
        return jsonify(return_room)

    def get(self):
        result = []
        for room in get_all_rooms():
            occupier = live_data.room_queue.get_each_rooms_occupiers()[room['roomName']].team
            if occupier:
                color = get_colour_of_team(occupier)
            else:
                occupier = 'Nobody'
                color = '#212121'
            timetable = get_time_table_of_room(room["_id"])
            item = {
                "location":
                    {"longitude": room["location"]["coordinates"][0],
                     "latitude": room["location"]["coordinates"][1]},
                "roomName": room["roomName"],
                "_id": str(room["_id"]),
                "occupier": {"color": color, "name": occupier},
                "currentLecture": get_full_name_of_current_lecture_in_room(room['_id']),
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
        data = live_data.quiz_queue(request.headers['uid'],
                                    request.headers['team'],
                                    request.headers['room'])
        return jsonify({'quiz-request': True, 'data': data})


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
        # if result:
        #     descriptor, game, = result
        #     return jsonify(
        #         {
        #             'gid': game.game_id,  # game_id: a 24 byte string to identify each game
        #             'pid': game.get_player_id(request.headers['uid']),  # player_id: 0 or 1 identifies player in game
        #             'opp-name': get_player_name(game.players[not game.get_player_id(request.headers['uid'])].uid),
        #             'opp-team': game.players[not game.get_player_id(request.headers['uid'])].team,
        #             'name': game.quiz_name,
        #             'quiz': game.question,  # quiz in the already specified format
        #             'game-ready': descriptor == 'game'  # unimportant
        #         }
        #     )
        return jsonify({'nothing': True}, result)


@api.resource('/quiz-answer')
class QuizAnswer(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid', 'result', 'outcome'])
    def post(self):
        """Answer the quiz."""
        live_data.game_queue.refresh(request.headers['gid'])
        live_data.game_queue.submit_answer(request.headers['gid'], int(request.headers['pid']),
                                           int(request.headers['outcome']))
        return jsonify({'quiz-answer': True})


@api.resource('/quiz-state')
class QuizState(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid'])
    def get(self):
        """Ask the server if the other player has answered yet, if yes show result."""
        live_data.game_queue.refresh(request.headers['gid'])
        if live_data.game_queue[request.headers['gid']].all_answered:
            result = live_data.game_queue[request.headers['gid']].get_result_for_player(int(request.headers['pid']))
            live_data.game_queue[request.headers['gid']].set_finished(int(request.headers['pid']))
            if live_data.game_queue[request.headers['gid']].is_finished:
                with suppress(ValueError): del live_data.game_queue[request.headers['gid']]
            if result == 'LOST': live_data.timedout_users(request.headers['uid'])
            return jsonify(result)

        return jsonify({'not yet answered': True})


@api.resource('/rally')
class Rally(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'room'])
    def post(self):
        """Manage Rally request."""
        if live_data.rally_timeout.add(request.headers['team'],
                                       request.headers['room'],
                                       get_player_name(request.headers['uid'])):
            return {'rally': True}
        return {'rally': False, 'reason': 'already rallying'}

    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team'])
    def get(self):
        """Manage Rally request."""
        return {'rally': live_data.rally_timeout.get(request.headers['team'])}



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
    @request_requires(headers=['uid', 'name'])
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


# @api.resource('/robin')
@api.resource('/live-debug')
class LiveDebug(Resource):
    def get(self):
        return jsonify(live_data.json)


@api.resource('/echo')
class Echo(Resource):
    def get(self):
        return 'Hallo Echo!', 200


if __name__ == '__main__':
    pass
