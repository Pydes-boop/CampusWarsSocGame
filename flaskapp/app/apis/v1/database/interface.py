#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ()

from apis.v1.database import mongo, db
from datetime import datetime
from apis.v1.database.time_functions import get_current_time_and_day, get_current_term
from bson.objectid import ObjectId


def find_closest_room(lon, lat, max_distance):
    return mongo.db.room.find_one({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lon, lat]},
                                                          "$maxDistance": max_distance}}}, {"_id": 0})


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


def add_lecture(name, term, room_id=None, timetable=[]):
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    item = {
        "name": name,
        "term": term,
        "roomID": room_id,
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


def add_lectures_to_user(firebase_id, lectures):
    lectures = lectures.split(",")
    for i in range(len(lectures)):
        lectures[i] = lectures[i][1:-1]
        split_string = lectures[i].split(":")
        name = split_string[0]
        term = split_string[1]
        entry_exists = mongo.db.lectures.count({"name": name, "term": term}, {limit: 1})
        lecture_id = None
        if entry_exists == 0:
            item = {
                "name": name,
                "term": term,
                "roomID": None,
                "timetable": []
            }
            result = mongo.db.lecture.insert_one(item)
            if not result.acknowledged:
                return False
            lecture_id = result.inserted_id
        else:
            lecture_id = mongo.db.lectures.find_one({"name": name, "term": term}, {"_id": 1})["_id"]
        if not mongo.db.firebase_users.update({"firebaseID": firebase_id},
                                              {"$push": {"lectures": lecture_id}}).acknowledged:
            return False

    return True


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
    current_time = get_current_time_and_day()
    index_lecture = mongo.db.lecture.find_one({"roomID": room_id, "term": get_current_term(),
                                               "timetable": {"$elemMatch": {"start": {"$lt": current_time[0]},
                                                                            "end": {"$gte": current_time[0]},
                                                                            "day": current_time[1]}}},
                                              {"_id": 1})
    indices_quizzes = mongo.db.quiz.find({"lectureID": index_lecture})
    return list(mongo.db.quiz.find({"_id": {"$in": indices_quizzes}}))


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
    lecture = mongo.db.lecture.find_one({"roomID": room_id, "term": get_current_term(),
                                         "timetable": {"$elemMatch": {"start": {"$lt": current_time[0]},
                                                                      "end": {"$gte": current_time[0]},
                                                                      "day": current_time[1]}}})
    if lecture is None:
        return None
    return lecture["name"] + ": " + lecture["term"]


def add_new_teams(team_list):
    for t in team_list:
        if not add_team(t):
            return False, t
    return True, None


def add_team(member_list):
    item = {
        "name": "teamname",
        "colour": "#333333",
        "term": get_current_term(),
        "members": member_list,
    }
    return mongo.db.teams.insert_one(item).acknowledged


def get_all_lecture_ids():
    return list(mongo.db.lecture.find({}, {"_id": 1}))


if __name__ == '__main__':
    pass
