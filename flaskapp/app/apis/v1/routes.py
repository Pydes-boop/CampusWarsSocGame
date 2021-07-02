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
import random
import json
from apis.v1.database import interface
from apis.v1.database.interface import add_room, add_lecture, get_all_rooms, find_closest_room, add_lectures_to_user, \
    add_question_to_quiz, add_user, get_users_of_lecture, get_full_name_of_current_lecture_in_room, get_current_team, \
    get_player_name, get_current_quizzes, get_questions_of_quiz, get_time_table_of_room, get_all_lecture_ids, \
    get_current_team_with_member_names, get_colour_of_team
from bson.objectid import ObjectId
from apis.v1.database.time_functions import get_current_term, get_time_as_seconds

from data_handler import live_data, team_state


@v1.app_errorhandler(404)
def error_404(_):
    return make_response(jsonify({'exception': 'Not found!', 'code': 404}), 404)


@api.resource('/roomfinder')
class RoomFinder(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'team', 'latitude', 'longitude'])
    def post(self):
        lat, lon, = map(float, [request.headers['longitude'], request.headers['latitude']])
        room = find_closest_room(lat, lon, 30)
        if room is None:
            return jsonify({"message": 'nothing near you'})
        name = room['roomName']
        team_state.increase_team_presence_in_room(team=request.headers['team'], room=name)
        live_data.room_queue(uid=request.headers['uid'], team=request.headers['team'], room=name)
        return_room = {"message": "closest room to you:",
                       'occupancy': team_state.get_all_team_scores_in_room(name),
                       'occupier': team_state.get_room_occupier(name),
                       'room_name': name, 'lid': str(room["_id"]),
                       'multiplier': team_state.mw[name].multiplier,
                       "currentLecture": get_full_name_of_current_lecture_in_room(str(room["_id"]))}
        return jsonify(return_room)

    # todo @Robin insert your stuff instead of my dummy stuff
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
        return jsonify('ok')


@api.resource('/quiz-request')
class QuizRequest(Resource):
    @check_timed_out_users(live_data.timedout_users)
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
        return jsonify(live_data.room_queue, live_data.quiz_queue,
                       dict([(key, item.json) for key, item in live_data.game_queue.items()]))


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
                    'opp-name': get_player_name(request.headers['uid']),
                    'opp-team': game.players[not game.get_player_id(request.headers['uid'])].team,
                    'name': game.name,
                    # name of the opponent team
                    'quiz': game.question,
                    # quiz in the already specified format TODO is there a way to get just a random quiz
                    'game-ready': descriptor == 'game'  # unimportant
                }
            )
        return jsonify('nothing')


@api.resource('/quiz-answer')
class QuizAnswer(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid', 'result', 'outcome'])
    def post(self):
        """Answer the quiz."""
        live_data.game_queue[request.headers['gid']].refresh()
        live_data.game_queue.submit_answer(request.headers['gid'], int(request.headers['pid']),
                                           int(request.headers['outcome']))
        return jsonify('ok')


@api.resource('/quiz-state')
class QuizState(Resource):
    @check_timed_out_users(live_data.timedout_users)
    @request_requires(headers=['uid', 'gid', 'pid'])
    def get(self):  # TODO maybe think about combining this with the request above
        """Ask the server if the other player has answered yet, if yes show result."""
        live_data.game_queue[request.headers['gid']].refresh()
        if live_data.game_queue[request.headers['gid']].all_answered:
            result = live_data.game_queue[request.headers['gid']].get_result_for_player(int(request.headers['pid']))
            if result == 'LOST': live_data.timedout_users(request.headers['uid'])
            return jsonify(result)

        return jsonify('not yet answered')


@api.resource('/echo')
class Echo(Resource):
    def get(self):
        return "Hallo Echo!", 200


@api.resource('/lectures')
class Lectures(Resource):
    def post(self):
        if "encoding_format" in request.headers:
            lectures = json.loads(request.headers["lectures"])
            lectures = list(map(lambda x: x.decode(request.headers["encoding_format"]).encode('utf8'), lectures))
            return add_lectures_to_user(request.headers["uid"], lectures)
        else:
            return add_lectures_to_user(request.headers["uid"], json.loads(request.headers["lectures"]))


@api.resource('/mygroup')
class MyGroup(Resource):
    @request_requires(headers=['uid'])
    def get(self):
        return jsonify(get_current_team_with_member_names(request.headers['uid']))


@api.resource('/start')
class Start(Resource):
    @request_requires(headers=['passphrase'])
    def post(self):
        if request.headers['passphrase'] == "YOU ONLY CALL THIS TWICE A YEAR PLS":
            if groupCreation.create_groups()[0]:
                return "ok", 200
            else:
                return "nope", 400


@api.resource('/question')
class Question(Resource):
    @request_requires(headers=['question', 'right_answer', 'wrong_answers', 'quiz_id'])
    def post(self):
        add_question_to_quiz(request.headers['question'], request.headers['right_answer'],
                             request.headers['wrong_answers'], request.headers['quiz_id'])
        return "ok", 200


@api.resource('/register')
class Register(Resource):
    def post(self):
        add_user(request.headers["uid"], request.headers["name"])
        return "ok", 200


@api.resource('/timetable')
class TimeTable(Resource):
    @request_requires(headers=['room_id'])
    def post(self):
        return get_time_table_of_room(request.headers['room_id'])


@api.resource('/marina')
class Test(Resource):
    def get(self):
        add_lecture("Einführung in die Theoretische Informatik (IN0011)", get_current_term(),
                    [{"start": get_time_as_seconds(14, 15), "end": get_time_as_seconds(16, 0),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"), "day": 0},
                     {"start": get_time_as_seconds(14, 15),
                      "end": get_time_as_seconds(16, 0),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 3},
                     ])
        add_lecture("Grundlagen Rechnernetze und Verteilte Systeme (IN0010)", get_current_term(),
                    [{"start": get_time_as_seconds(10, 0),
                      "end": get_time_as_seconds(12, 0),
                      "roomID": ObjectId("60d789da1ca97fc034f1f5ab"),
                      "day": 0},
                     {"start": get_time_as_seconds(10, 0),
                      "end": get_time_as_seconds(12, 0),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 1},
                     ])
        add_lecture("Grundlagen: Algorithmen und Datenstrukturen (IN0007)", get_current_term(),
                    [{"start": get_time_as_seconds(14, 0),
                      "end": get_time_as_seconds(16, 0),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 1},
                     {"start": get_time_as_seconds(13, 15),
                      "end": get_time_as_seconds(14, 15),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 2},
                     ])
        add_lecture("Marina Test Lecture (7777)", get_current_term(),
                    [{"start": get_time_as_seconds(14, 0),
                      "end": get_time_as_seconds(16, 0),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 1},
                     {"start": get_time_as_seconds(13, 15),
                      "end": get_time_as_seconds(18, 15),
                      "roomID": ObjectId("60d78a721ca97fc034f1f5ac"),
                      "day": 3},
                     ])
        add_user("1", "Hans", ["Englisch - English through Cinema C1: 20W", "Diskrete Strukturen (IN0015): 19W",
                               "Einführung in die Informatik 1 (IN0001): 19W", "Französisch A1.1: 19W",
                               "Social Gaming (IN0040): 21S", "Studentische Vollversammlungen - Informatik: 20W",
                               "Praktikum: Echtzeit-Computergrafik (IN0039): 21S",
                               "Analysis für Informatik [MA0902]: 20W",
                               "Übungen zu Analysis für Informatik [MA0902]: 20W", "Interaktive Visualisierung: 20W",
                               "Einführung in Informatik für Games Engineering (IN0031): 19W"])

        add_user("2", "Franz",
                 ["Englisch - English through Cinema C1: 20S", "Studentische Vollversammlungen - Informatik: 21S",
                  "Praktikum: Grundlagen der Programmierung (IN0002), Di, Mi: 19W",
                  "Echtzeit-Computergrafik (IN0038): 21S", "Ringvorlesung 'Games Engineering' (IN2368): 21S",
                  "Social Gaming (IN0040): 21S", "Einführung in die Theoretische Informatik (IN0011): 21S",
                  "Einführung in die Informatik 1 (IN0001): 19W", "Audiokommunikation: 21S",
                  "Studentische Vollversammlungen - Informatik: 19W", "Interaktive Visualisierung: 20W"])

        add_user("3", "Peter",
                 ["Praktikum: Echtzeit-Computergrafik (IN0039): 21S", "Englisch - English through Cinema C1: 20W",
                  "Übungen zu Analysis für Informatik [MA0902]: 20W",
                  "Einführung in die Theoretische Informatik (IN0011): 21S",

                  "Praktikum: Grundlagen der Programmierung (IN0002), Di, Mi: 19W", "Französisch A1.1: 19W",
                  "Übungen zu Einführung in Informatik für Games Engineering(IN0031): 19W",
                  "Studentische Vollversammlungen - Informatik: 19W", "Analysis für Informatik [MA0902]: 20W",
                  "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S",
                  "Studentische Vollversammlungen - Informatik: 21S"])
        add_user("4", "Lisa",
                 ["Praktikum: Echtzeit-Computergrafik (IN0039): 21S",
                  "Praktikum: Grundlagen der Programmierung (IN0002), Di, Mi: 19W",
                  "Interaktionsmethoden und -geräte (IN0033): 20W", "Englisch - English through Cinema C1: 20S",
                  "Englisch - English through Cinema C1: 20W",
                  "Einführung in die Theoretische Informatik (IN0011): 21S", "Social Gaming (IN0040): 21S",
                  "Einführung in Informatik für Games Engineering (IN0031): 19W",
                  "Numerisches Programmieren (IN0019): 21S",
                  "Grundlagen: Algorithmen und Datenstrukturen (IN0007): 20S",
                  "Studentische Vollversammlungen - Informatik: 20S"])

        add_user("5", "Klara",
                 ["Englisch - English through Cinema C1: 20W", "Interaktive Visualisierung: 20W",
                  "Studentische Vollversammlungen - Informatik: 21S",
                  "Übungen zu Lineare Algebra für Informatik [MA0901]: 20S",
                  "Praktikum Social Gaming (IN0041): 21S",
                  "Übungen zu Einführung in Informatik für Games Engineering(IN0031): 19W",
                  "Studentische Vollversammlungen - Informatik: 19W",
                  "Einführung in die Theoretische Informatik (IN0011): 21S",
                  "Modellierung mit Blender (IN2282): 20W", "Studentische Vollversammlungen - Informatik: 20S",
                  "Analysis für Informatik [MA0902]: 20W"])
        add_user("6", "Johannes",
                 ["Betriebssysteme und hardwarenahe Programmierung für Games (IN0034): 20W",
                  "Studentische Vollversammlungen - Informatik: 20S", "Numerisches Programmieren (IN0019): 21S",
                  "Übungen zu Einführung in die Theoretische Informatik (IN0011), Mo, Di, Fr: 21S",
                  "Modellierung mit Blender (IN2282): 20W", "Echtzeit-Computergrafik (IN0038): 20S",
                  "Ringvorlesung 'Games Engineering' (IN2368): 21S",
                  "Übungen zu Diskrete Strukturen (IN0015) - 1 (Mo): 19W", "Grundlagen: Datenbanken (IN0008): 20W",
                  "Interaktionsmethoden und -geräte (IN0033): 20W", "Englisch - English through Cinema C1: 20S"])
        add_user("7", "Mimi",
                 ["Numerisches Programmieren (IN0019): 21S", "Ringvorlesung 'Games Engineering' (IN2368): 21S",
                  "Lineare Algebra für Informatik [MA0901]: 20S",
                  "Studentische Vollversammlungen - Informatik: 20S",
                  "Übungen zu Interaktionsmethoden und -geräte (IN0033): 20W",
                  "Echtzeit-Computergrafik (IN0038): 21S",
                  "Übungen zu Einführung in die Softwaretechnik (IN0006) 27 Gruppen: 20S",
                  "Einführung in die Informatik 1 (IN0001): 19W",
                  "Praktikum: Echtzeit-Computergrafik (IN0039): 21S", "Englisch - English through Cinema C1: 20S",
                  "Übungen zu Grundlagen: Algorithmen und Datenstrukturen (IN0007), Mo, Di: 20S"])
        add_user("8", "Pokemon",
                 ["Echtzeit-Computergrafik (IN0038): 20S", "Grundlagen der Künstlichen Intelligenz (IN2062): 20W",
                  "Grundlagen: Algorithmen und Datenstrukturen (IN0007): 20S", "Französisch A1.1: 19W",
                  "Englisch - English through Cinema C1: 20W",
                  "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S",
                  "Studentische Vollversammlungen - Informatik: 20S",
                  "Praktikum: Echtzeit-Computergrafik (IN0039): 20S", "Ringvorlesung 'Games Engineering' (IN2368): 21S",
                  "Diskrete Strukturen (IN0015): 19W",
                  "Lineare Algebra für Informatik [MA0901]: 20S"])
        add_user("9", "Sophie",
                 ["Modellierung mit Blender (IN2282): 20W",
                  "Übungen zu Einführung in die Softwaretechnik (IN0006) 27 Gruppen: 20S",
                  "Praktikum: Echtzeit-Computergrafik (IN0039): 20S", "Echtzeit-Computergrafik (IN0038): 21S",
                  "Audiokommunikation: 21S", "Praktikum Social Gaming (IN0041): 21S",
                  "Studentische Vollversammlungen - Informatik: 20S",
                  "Übungen zu Grundlagen: Algorithmen und Datenstrukturen (IN0007), Mo, Di: 20S",
                  "Übungen zu Diskrete Strukturen (IN0015) - 1 (Mo): 19W", "Geschichtswelten (IN2290): 20W",
                  "Studentische Vollversammlungen - Informatik: 19W"])
        add_user("10", "Hannes",
                 ["Übungen zu Analysis für Informatik [MA0902]: 20W", "Diskrete Strukturen (IN0015): 20W",
                  "Englisch - English through Cinema C1: 20W", "Studentische Vollversammlungen - Informatik: 19W",
                  "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S",
                  "Praktikum: Echtzeit-Computergrafik (IN0039): 21S",
                  "Einführung in die Theoretische Informatik (IN0011): 21S",
                  "Grundlagen der Künstlichen Intelligenz (IN2062): 20W",
                  "Übungen zu Grundlagen: Algorithmen und Datenstrukturen (IN0007), Mo, Di: 20S",
                  "Echtzeit-Computergrafik (IN0038): 21S",
                  "Übungen zu Einführung in Informatik für Games Engineering(IN0031): 19W"])
        return "success"


if __name__ == '__main__':
    pass
