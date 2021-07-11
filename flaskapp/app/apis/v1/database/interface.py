#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
In this file, we define functions necessary so we can communicate effectively with our database.
As recommended by the mongodb documentation (https://docs.mongodb.com/), we use lowercase with camelCase for the db,
while we use all lowercases with _ spaces for python

"""

__all__ = (
    "add_room",
    "add_lecture",
    "get_all_rooms",
    "find_closest_room",
    "add_lectures_to_user",
    "add_question_to_quiz",
    "add_user",
    "get_users_of_lecture",
    "get_full_name_of_current_lecture_in_room",
    "get_current_team",
    "get_player_name",
    "get_current_quizzes",
    "get_questions_of_quiz",
    "get_colour_of_team",
)

import groupCreation
from apis.v1.database import mongo, db
from datetime import datetime
from apis.v1.utils.time_functions import (
    get_current_time_and_day,
    get_current_term,
    get_day_as_string,
    get_seconds_as_string,
)
from bson.objectid import ObjectId


def find_closest_room(lon, lat, max_distance):
    """
    Finds the room closest to the given longitude & latitude. If there is no room close than max_distance, None is
    returned.

    Parameters:
        lon (float): longitude of the position
        lat (float): latitude of the position
        max_distance (float): the maximum distance that may be between a room and the position for it to be considered

    Returns:
        (dict): A dictionary with the room information if a room was found, None otherwise

    Description of the keys and their values of the returned dict:
        _id: The generated _id of the room
        location: the location of the room, format: {"type": "Point", "coordinates": [longitude,latitude]}
        roomName: the name of the room
        campusID: The id of the campus that room belongs to

    """
    return mongo.db.room.find_one(
        {
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": max_distance,
                }
            }
        }
    )


def add_room(room_name, longitude, latitude, campus_id=None):
    """
    Adds a room to the database

    Parameters:
        room_name(str): the roomName of the room that should be added
        longitude (float): the longitude of the position of the room
        latitude (float): the latitude of the position of the room

    Returns:
        (bool): True, if successfully added, False otherwise
    """
    item = {
        "location": {"type": "Point", "coordinates": [longitude, latitude]},
        "roomName": room_name,
    }
    return mongo.db.room.insert_one(item).acknowledged


def get_all_rooms():
    """
    Returns all rooms that are stored in the database.

    Returns:
        (list of dicts): the list with all rooms stored in the database.

     Description of the keys and their values of the returned dicts:
        _id: The generated _id of the room
        location: the location of the room, format: {"type": "Point", "coordinates": [longitude,latitude]}
        roomName: the name of the room
        campusID: The id of the campus that room belongs to
    """
    return list(mongo.db.room.find())


def add_lecture(name, term, timetable=[]):
    """
    adds a new lecture to the database. If the lecture already exists in the database, only the new entries of the
    timetable are added instead.

    Parameters:
        name (str): Name of the lecture
        term (str): The term in which the lecture is held
        timetable (list of dicts): The time schedule for the lecture

    Returns:
        (boo): True, if the lecture was successfully added to the database or all the new entries of the timetable
        were successfully added, False otherwise

    """
    if timetable is None:
        timetable = []
    entry = mongo.db.lecture.find_one({"name": name, "term": term})
    if entry is None:  # Entry does not already exist in db, create new one
        item = {"name": name, "term": term, "timetable": timetable}
        return mongo.db.lecture.insert_one(item).acknowledged
    for t in timetable:  # add entries of timetable that do not already exist in the db
        if any(
            e["start"] == t["start"]
            and e["end"] == t["end"]
            and e["roomID"] == t["roomID"]
            and e["day"] == t["day"]
            for e in entry["timetable"]
        ):
            continue
        elif not any(
            e["start"] < t["end"]
            and e[  # test if there is no overlapping with previously added entries
                "end"
            ]
            > t["start"]
            and e["day"] == t["day"]
            for e in entry["timetable"]
        ):
            if (
                not mongo.db.lecture.update_one(
                    {"_id": entry["_id"]}, {"$push": {"timetable": t}}
                ).matched_count
                > 0
            ):
                return False
        else:
            return False

    return True


def add_user(firebase_id, name, lectures=[]):
    """
    adds a new user to the database. If the user already exists, only the new lectures will be added to the users'
    lectures list

    Parameters:
        firebase_id(str): the Firebase ID of the user
        name(str): The user name
        lectures(list of ObjectId): the list of lectures the user attended/attends

    Returns:
        (bool): True, if successfully added the new user / the lectures, False otherwise

    """
    if lectures is None:
        lectures = []
    entry = mongo.db.firebase_users.find_one({"firebaseID": firebase_id})
    if entry is None:
        item = {"firebaseID": firebase_id, "name": name, "lectures": lectures}
        return mongo.db.firebase_users.insert_one(item).acknowledged
    else:
        for lec in lectures:
            if lec not in entry["lectures"]:
                if (
                    not mongo.db.firebase_users.update_one(
                        {"_id": entry["_id"]}, {"$push": {"lectures": lec}}
                    ).matched_count
                    > 0
                ):
                    return False
        return True


def add_lectures_to_user(firebase_id, lectures):
    """
    adds the lectures given to the list of lectures attended by the user. The list, however, is a list of strings and
    is not in the right format for our database
    Given format: <lecture name>:<term>
    Wanted format: two strings: 1. <lecture name>, 2. <term>

    Parameters:
        firebase_id (str): the firebase ID of the user that the lectures belong to
        lectures (list of str): The list of the lectures the user attended

    Returns:
        (bool): True, if all the insertions were successful, False otherwise

    """
    for i in range(len(lectures)):
        split_string = lectures[i].split(":")
        name = split_string[0]
        j = 1
        while j < len(split_string) - 1:
            name += split_string[j]
            j = j + 1
        term = split_string[j][1:]
        if not add_lecture(name, term):
            return False
        lecture_id = mongo.db.lecture.find_one(
            {"name": name, "term": term}, {"_id": 1}
        )["_id"]
        if (
            not mongo.db.firebase_users.update_one(
                {"firebaseID": firebase_id}, {"$push": {"lectures": lecture_id}}
            ).matched_count
            > 0
        ):
            return False
    return True


def add_question_to_quiz(question, right_answer, wrong_answers, quiz_id):
    """
    Adds a question to a quiz into the database.

    Parameters:
        question(str): The question text of the question
        right_answer(str): The right answer
        wrong_answers(list of str): The wrong answers
        quiz_id: The ID of the quiz the question belongs to

    Returns: True, if insertion was successful, False otherwise
    """
    if isinstance(quiz_id, str):
        quiz_id = ObjectId(quiz_id)
    item = {
        "question": question,
        "rightAnswer": right_answer,
        "wrongAnswers": wrong_answers,
        "quizID": quiz_id,
    }
    return mongo.db.question.insert_one(item)["acknowledged"]


def get_current_quizzes(room_id):
    """ """
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    lecture = get_current_lecture(room_id)
    room_info = mongo.db.room.find_one({"_id": room_id}, {"_id": 0})
    if lecture is None:
        return list(mongo.db.quiz.find({"campusID": room_info["campusID"]}))
    result = list(mongo.db.quiz.find({"lectureID": lecture["_id"]}))
    if len(result) == 0:
        return list(mongo.db.quiz.find({"campusID": room_info["campusID"]}))
    return result


def get_current_lecture(room_id):
    current_time = get_current_time_and_day()
    return mongo.db.lecture.find_one(
        {
            "term": get_current_term(),
            "timetable": {
                "$elemMatch": {
                    "start": {"$lt": current_time["seconds"]},
                    "end": {"$gte": current_time["seconds"]},
                    "roomID": room_id,
                    "day": current_time["day"],
                }
            },
        }
    )


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
    user = mongo.db.firebase_users.find_one({"firebaseID": firebase_id})
    if user is not None:
        return user["lectures"]
    return None


def get_users_of_lecture(lecture_id):
    if isinstance(lecture_id, str):
        lecture_id = ObjectId(lecture_id)
    items = []
    return list(
        map(
            lambda x: str(x["firebaseID"]),
            list(
                mongo.db.firebase_users.find(
                    {"lectures": {"$elemMatch": {"$eq": lecture_id}}},
                    {"firebaseID": 1, "_id": 0},
                )
            ),
        )
    )


def get_full_name_of_current_lecture_in_room(room_id):
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    lecture = get_current_lecture(room_id)

    if lecture is None:
        return None
    return lecture["name"] + ": " + lecture["term"]


def get_time_table_of_room(room_id):
    if isinstance(room_id, str):
        room_id = ObjectId(room_id)
    lectures = list(
        mongo.db.lecture.find(
            {
                "term": get_current_term(),
                "timetable": {"$elemMatch": {"roomID": room_id}},
            }
        )
    )
    items = []
    for lec in lectures:
        for e in lec["timetable"]:
            if e["roomID"] == room_id:
                items.append(
                    {
                        "name": lec["name"] + ": " + lec["term"],
                        "day_as_int": e["day"],
                        "day": get_day_as_string(e["day"]),
                        "start": get_seconds_as_string(e["start"]),
                        "end": get_seconds_as_string(e["end"]),
                    }
                )
    items = sorted(items, key=lambda x: (x["day_as_int"], x["start"]))
    return items


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
    return list(map(lambda x: str(x["_id"]), list(mongo.db.lecture.find())))


def get_player_name(firebase_id):
    user = mongo.db.firebase_users.find_one({"firebaseID": firebase_id}, {"name": 1})
    if user is None:
        return None
    return user["name"]


def get_current_team_with_member_names(firebase_id):
    my_team = get_current_team(firebase_id)
    if my_team is None:
        return None
    my_team["members"] = list(map(lambda x: get_player_name(x), my_team["members"]))
    return my_team


def get_questions_of_quiz(quiz_id):
    return list(mongo.db.question.find({"quizID": quiz_id}, {"_id": 0, "quizID": 0}))


def get_current_team(firebase_id):
    return mongo.db.teams.find_one(
        {"members": {"$elemMatch": {"$eq": firebase_id}}, "term": get_current_term()},
        {"_id": 0},
    )


def get_colour_of_team(team_name):
    result = mongo.db.teams.find_one({"name": team_name, "term": get_current_term()})
    if result is None:
        return "#212121"
    return result["colour"]


def get_escaped_by_db(text):
    mongo.db.text.insert_one({"text": text})
    returned_text = mongo.db.text.find_one()["text"]
    mongo.db.text.delete_many({})
    return returned_text


def get_quiz_info(quiz_id):
    if isinstance(quiz_id, str):
        quiz_id = ObjectId(quiz_id)
    return mongo.db.quiz.find_one({"_id": quiz_id})


def get_number_of_players():
    return len(list(mongo.db.firebase_users.find()))


def get_all_lecture_names():
    return mongo.db.lecture.find({}, {"name": 1})


# def get_all_teams():
#  return str(list(mongo.db.teams.find()))


if __name__ == "__main__":
    pass
