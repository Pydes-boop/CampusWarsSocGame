#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ()

from apis.v1.database import mongo, db
from datetime import datetime
from apis.v1.database.time_functions import get_current_time_in_millis, get_current_term


def find_closest_room(lon, lat, max_distance):
    return mongo.db.room.find_one({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lon, lat]},
                                                          "$maxDistance": max_distance}}}, {"_id": 0})


# todo evtl occupier live im Überblick behalten weil wegen regelmäßiges update ähnlich der location vom user
#  @Felix,Robin
def add_room(room_name, longitude, latitude):
    item = {
        "type": "Point",
        "coordinates": [longitude, latitude],
        "roomName": room_name,
    }
    return mongo.db.room.insert_one(item)['acknowledged']


def get_all_rooms():
    return list(mongo.db.room.find({}, {"_id": 0}))


def add_lecture(name, term, room_id=None, timetable=[]):
    item = {
        "name": name,
        "term": term,
        "roomID": room_id,
        "timetable": timetable
    }
    return mongo.db.lecture.insert_one(item)['acknowledged']


def add_user(firebase_id, name, lectures=[]):
    if lectures is None:
        lectures = []
    item = {
        "firebaseID": firebase_id,
        "name": name,
        "lectures": lectures
    }
    return mongo.db.firebase_users.insert_one(item)['acknowledged']


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
            if not result['acknowledged']:
                return False
            lecture_id = result['insertedId']
        else:
            lecture_id = mongo.db.lectures.find_one({"name": name, "term": term}, {"_id": 1})["_id"]
        if not mongo.db.firebase_users.update({"firebaseID": firebase_id},
                                              {"$push": {"lectures": lecture_id}})['acknowledged']:
            return False

    return True


def add_question_to_quiz(question, right_answer, wrong_answers, quiz_id):
    item = {
        "question": question,
        "rightAnswer": right_answer,
        "wrongAnswers": wrong_answers,
        "quizID": quiz_id
    }
    return mongo.db.question.insert_one(item)['acknowledged']


def get_current_quizzes(room_id):
    current_time = get_current_time_in_millis()
    index_lecture = mongo.db.lecture.find_one({"roomID": room_id, "term": get_current_term(),
                                               "timetable": {"$elemMatch": {"start": {"$lt": current_time},
                                                                            "end": {"$gte": current_time}}}},
                                              {"_id": 1})
    indices_quizzes = mongo.db.quiz.find({"lectureID": index_lecture})
    return list(mongo.db.quiz.find({"_id": {"$in": indices_quizzes}}))


def add_quiz(name, created_by, lecture):
    item = {
        "name": name,
        "createdBy": created_by,
        "lectureID": lecture,
        "creationDate": datetime.now().isoformat(),
    }
    return mongo.db.quiz.insert_one(item)['acknowledged']


def get_lectures_of_user(firebase_id):
    return mongo.db.users.find_one({"firebaseID": firebase_id})["lectures"]


def get_users_of_lecture(lecture_id):
    return list(mongo.db.users.find({"lectures": lecture_id}, {"firebaseID": 1}))


if __name__ == '__main__':
    pass
