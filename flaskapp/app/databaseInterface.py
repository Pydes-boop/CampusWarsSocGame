__all__ = ('application', 'get_all_rooms', 'add_room')

import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

max_distance = 30

application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db


def room_detection(lat, lon):
    return db.room.findOne({"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lat, lon]}}}})


def add_room(room_name, longitude, latitude):
    item = {
        "type": "Point",
        "coordinates": [longitude, latitude],
        "roomName": room_name,
        "occupier": None
    }
    db.room.insert_one(item)


def get_all_rooms():
    item = {}
    data = []
    for entry in db.room.find({}):
        item = {
            'id': str(entry['_id']),
            'room_name': entry['roomName']
        }
        data.append(item)
    return data


def get_all_groups():
    ...
    return [{'name': 'IMGE 2019'},
            {'name': 'DS 2021'}]


def set_user_groups(user, groups):
    ...
    return "User Group X"
    # return "null"


def add_question(question, right_answer, wrong_answers):
    ...


# returns closest room, if any is close enough, otherwise null
def find_next_room(longitude, latitude):
    ...
