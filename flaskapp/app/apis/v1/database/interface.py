#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ()

from apis.v1.database import mongo, db
from datetime import datetime
from time import time


def room_detection(lat, lon, max_distance):
    return mongo.db.room.find_one({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lat, lon]},
                                                          "$maxDistance": max_distance}}})


# todo evtl occupier live im Überblick behalten weil wegen regelmäßiges update ähnlich der location vom user
#  @Felix,Robin
def add_room(room_name, longitude, latitude):
    item = {
        "type": "Point",
        "coordinates": [longitude, latitude],
        "roomName": room_name,
        "occupier": None
    }
    return mongo.db.room.insert_one(item)['acknowledged']


def get_all_rooms():
    data = []
    for entry in mongo.db.room.find({}):
        item = {
            'room_name': entry['roomName'],
            'longitude': entry['coordinates'][0],
            'latitude': entry['coordinates'][1],
            'occupier': entry['occupier']
        }
        data.append(item)
    return data


def get_all_groups():
    # might be unnecessary because the tum online interface gets the possible groups
    return mongo.db.group.find({})


def add_main_lecture(name, term, room_id, timetable):
    item = {
        "name": name,
        "term": term,
        "subgroup_of": None,
        "roomID": room_id,
        "timetable": timetable
    }
    return mongo.db.lecture.insert_one(item)['acknowledged']


def add_lecture(name, term, supergroup, room_id):
    item = {
        "name": name,
        "term": term,
        "subgroup_of": supergroup,
        "roomID": room_id,
        "timetable": timetable
    }
    return mongo.db.lecture.insert_one(item)['acknowledged']


# todo add unique identifier for players
def add_user(firebase_id, first_name, last_name, lectures):
    if lectures is None:
        lectures = []
    item = {
        "firebaseID": firebase_id,
        "firstName": first_name,
        "lastName": last_name,
        "lectures": lectures
    }
    return mongo.db.firebase_users.insert_one(item)['acknowledged']


# todo wie converten @Felix???
def set_user_groups_group_string(firebase_id, groups):
    lectures = groups.split(",")
    for i in range(len(lectures)):
        lectures[i] = lectures[i][1:-1]
    # todo: @Marina add uid{str} and lectures{list{str}} to database

    return set_user_groups(firebase_id, lectures)


def set_user_groups(firebase_id, groups):
    return mongo.db.user.update({"firebaseID": firebase_id}, {"$set": {"groups": groups}})


def add_question_to_quiz(question, right_answer, wrong_answers, lecture_id, quiz_id):
    item = {
        "question": question,
        "rightAnswer": right_answer,
        "wrongAnswers": wrong_answers,
        "lectureID": lecture_id,
        "quizID": quiz_id
    }
    return mongo.db.question.insert_one(item)['acknowledged']


# todo we need to ask between certain times
def get_current_quizzes(room_id):
    current_time = round(time.time() * 1000)
    indices = mongo.db.groups.find_all({"roomID": room_id})
    indices_quizzes = mongo.db.groups.find_all({"groupID": {"$in": indices}})
    return mongo.db.quiz.find_all({"_id": {"$in": indices_quizzes}},
                                  {"timetable": {
                                      "$elemMatch": {"start": {"$lt": current_time}, "end": {"$gte": current_time}}}})


def add_quiz(name, created_by, group):
    item = {
        "name": name,
        "createdBy": created_by,
        "groupID": group,
        "creationDate": datetime.now().isoformat(),
    }
    return mongo.db.quiz.insert_one(item)['acknowledged']


if __name__ == '__main__':
    pass
