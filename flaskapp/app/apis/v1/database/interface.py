#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ("add_room", "add_lecture", "get_all_rooms", "find_closest_room", "add_lectures_to_user",
           "add_question_to_quiz", "add_user", "get_users_of_lecture", "get_full_name_of_current_lecture_in_room",
           "get_current_team", "get_player_name", "get_current_quizzes", "get_questions_of_quiz", "get_colour_of_team")

from apis.v1.database import mongo, db
from datetime import datetime
from apis.v1.database.time_functions import get_current_time_and_day, get_current_term
from bson.objectid import ObjectId


def find_closest_room(lon, lat, max_distance):
    return mongo.db.room.find_one({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lon, lat]},
                                                          "$maxDistance": max_distance}}})


# todo evtl occupier live im Überblick behalten weil wegen regelmäßiges update ähnlich der location vom user
#  @Felix,Robin
def add_room(room_name, longitude, latitude):
    item = {
        "location":
            {"type": "Point",
             "coordinates": [longitude, latitude]},
        "roomName": room_name,
    }
    return mongo.db.room.insert_one(item).acknowledged


def get_all_rooms():
    return list(mongo.db.room.find())


def add_lecture(name, term, timetable=[]):
    item = {
        "name": name,
        "term": term,
        "timetable": timetable
    }
    return mongo.db.lecture.insert_one(item).acknowledged


def add_user(firebase_id, name, lectures=[]):
    if lectures is None:
        lectures = []
    item = {
        "firebaseID": firebase_id,
        "name": name,
        "lectures": lectures
    }
    return mongo.db.firebase_users.insert_one(item).acknowledged


# todo schöner machen mit exists
def add_lectures_to_user(firebase_id, lectures):
    for i in range(len(lectures)):
        split_string = lectures[i].split(":")
        name = split_string[0]
        j = 1
        while j < len(split_string) - 1:
            name += split_string[j]
            j = j + 1
        term = split_string[j][1:]
        entry_exists = len(list(mongo.db.lectures.find({"name": name, "term": term}))) > 0
        lecture_id = None
        if not entry_exists:
            item = {
                "name": name,
                "term": term,
                "timetable": []
            }
            result = mongo.db.lecture.insert_one(item)
            if not result.acknowledged:
                return False
            lecture_id = result.inserted_id
        else:
            lecture_id = mongo.db.lecture.find_one({"name": name, "term": term}, {"_id": 1})["_id"]
        # todo why dict
        if mongo.db.firebase_users.update_one({"firebaseID": firebase_id},
                                              {"$push": {"lectures": lecture_id}}).matched_count == 0:
            return False

    return list(mongo.db.lecture.find({}, {"_id": 0}))


def add_question_to_quiz(question, right_answer, wrong_answers, quiz_id):
    if isinstance(quiz_id, str):
        quiz_id = ObjectId(quiz_id)
    item = {
        "question": question,
        "rightAnswer": right_answer,
        "wrongAnswers": wrong_answers,
        "quizID": quiz_id
    }
    return mongo.db.question.insert_one(item)['acknowledged']


def get_current_quizzes(room_id):
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    room_info = mongo.db.room.find_one({"_id": room_id}, {"_id": 0})
    return list(mongo.db.quiz.find({"campusID": room_info["campusID"]}))


def add_quiz(name, created_by, lecture_id):
    if isinstance(lecture_id, str):
        lecture_id = ObjectId(lecture_id)
    item = {
        "name": name,
        "createdBy": created_by,
        "lectureID": lecture_id,
        "creationDate": datetime.now().isoformat(),
    }
    return mongo.db.quiz.insert_one(item).acknowledged


def add_campus_quiz(name, created_by, campus_id):
    if isinstance(campus_id, str):
        campus_id = ObjectId(campus_id)
    item = {
        "name": name,
        "createdBy": created_by,
        "campusID": campus_id,
        "creationDate": datetime.now().isoformat(),
    }
    return mongo.db.quiz.insert_one(item).acknowledged


def get_lectures_of_user(firebase_id):
    return mongo.db.firebase_users.find_one({"firebaseID": firebase_id})["lectures"]


def get_users_of_lecture(lecture_id):
    if isinstance(lecture_id, str):
        lecture_id = ObjectId(lecture_id)
    return list(
        mongo.db.firebase_users.find({"lectures": {"$elemMatch": {"$eq": lecture_id}}}, {"firebaseID": 1, "_id": 0}))


# todo marina
def get_full_name_of_current_lecture_in_room(room_id):
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    current_time = get_current_time_and_day()
    lecture = mongo.db.lecture.find_one({"term": get_current_term(),
                                         "timetable": {"$elemMatch": {"start": {"$lt": current_time[0]},
                                                                      "end": {"$gte": current_time[0]},
                                                                      "roomID": room_id,
                                                                      "day": current_time[1]}}})

    if lecture is None:
        return None
    return lecture["name"] + ": " + lecture["term"]


def add_new_teams(team_list):
    mongo.db.teams.delete_many({"term": get_current_term()})
    for team in team_list:
        if not add_team(team):
            return False, team
    return True, None


def add_team(team):
    item = {
        "name": team.name,
        "colour": team.color,
        "term": get_current_term(),
        "members": team.members,
    }
    return mongo.db.teams.insert_one(item).acknowledged


def get_all_lecture_ids():
    return list(mongo.db.lecture.find({}, {"_id": 1}))


def get_player_name(firebase_id):
    return mongo.db.firebase_users.find_one({"firebaseID": firebase_id}, {"name": 1})


def get_questions_of_quiz(quiz_id):
    return list(mongo.db.question.find({"quizID": quiz_id}, {"_id": 0, "quizID": 0}))


def get_current_team(member_firebase_id):
    item = mongo.db.teams.find_one({"members": {"$elemMatch": {"$eq": member_firebase_id}}, "term": get_current_term()})
    item['_id'] = str(item['_id'])
    return item


def get_colour_of_team(team_name):
    return mongo.db.teams.find_one({"name": team_name, "term": get_current_term()})['colour']


def get_quiz_info(quiz_id):
    if isinstance(quiz_id, str):
        quiz_id = ObjectId(quiz_id)
    return mongo.db.quiz.find_one({"_id": quiz_id})


if __name__ == '__main__':
    pass
