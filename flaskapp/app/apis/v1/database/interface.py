#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-09"
__version__ = "0.0.1"

__all__ = ()

from apis.v1.database import mongo, db


def room_detection(lat, lon):
    return mongo.db.room.findOne({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lat, lon]}}}})


def add_room(room_name, longitude, latitude):
    item = {
        "type": "Point",
        "coordinates": [longitude, latitude],
        "roomName": room_name,
        "occupier": None
    }
    mongo.db.room.insert_one(item)


def get_all_rooms():
    item = {}
    data = []
    for entry in mongo.db.room.find({}):
        item = {
            'id': str(entry['_id']),
            'room_name': entry['roomName']
        }
        data.append(item)
    return data


def get_all_groups():
    return [{'name': 'IMGE 2019'},
            {'name': 'DS 2021'}]


def set_user_groups(user, groups):
    return "User Group X"
    # return "null"


def add_question(question, right_answer, wrong_answers):
    pass


# returns closest room, if any is close enough, otherwise null
def find_next_room(longitude, latitude):
    pass


if __name__ == '__main__': pass
