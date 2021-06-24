#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ()

from apis.v1.database import mongo, db
from datetime import datetime
from time import time


def find_closest_room(lat, lon, max_distance):
    return mongo.db.room.find_one({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lat, lon]},
                                                          "$maxDistance": max_distance}}})


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
    data = []
    for entry in mongo.db.room.find({}):
        item = {
            'room_name': entry['roomName'],
            'longitude': entry['coordinates'][0],
            'latitude': entry['coordinates'][1],
        }
        data.append(item)
    return data


def add_main_lecture(name, term, room_id=None, timetable=[]):
    item = {
        "name": name,
        "term": term,
        "sublectureOf": None,
        "roomID": room_id,
        "timetable": timetable
    }
    return mongo.db.lecture.insert_one(item)['acknowledged']


def add_lecture(name, term, supergroup, room_id, timetable):
    item = {
        "name": name,
        "term": term,
        "sublectureOf": supergroup,
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
        name = split_string[0].split()
        term = split_string[1].split()
        entry_exists = mongo.db.lectures.count({"name": name, "term": term}, {limit: 1})
        lecture_id = None
        if entry_exists == 0:
            item = {
                "name": name,
                "term": term,
                "sublectureOf": None,
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


def add_question_to_quiz(question, right_answer, wrong_answers, lecture_id, quiz_id):
    item = {
        "question": question,
        "rightAnswer": right_answer,
        "wrongAnswers": wrong_answers,
        "lectureID": lecture_id,
        "quizID": quiz_id
    }
    return mongo.db.question.insert_one(item)['acknowledged']


def get_current_quizzes(room_id):
    current_time = round(time.time() * 1000)
    index_lecture = mongo.db.lecture.find_one({"roomID": room_id,
                                               "timetable": {"$elemMatch": {"start": {"$lt": current_time},
                                                                            "end": {"$gte": current_time}}}},
                                              {"_id": 1})
    indices_quizzes = mongo.db.quiz.find_all({"lectureID": index_lecture})
    return mongo.db.quiz.find_all({"_id": {"$in": indices_quizzes}})


def add_quiz(name, created_by, lecture):
    item = {
        "name": name,
        "createdBy": created_by,
        "lectureID": lecture,
        "creationDate": datetime.now().isoformat(),
    }
    return mongo.db.quiz.insert_one(item)['acknowledged']


if __name__ == '__main__':
    pass
