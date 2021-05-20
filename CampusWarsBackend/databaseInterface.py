# todo: marina pls connect to database
def room_detection(lat, lon):
    ...
    # return {"room_name": "null", "occupier": "null"}
    return {"room_name": "test", "occupier": "Jonas und Robin"}


def get_all_rooms():
    ...
    return [{'name': 'MW-1', 'location': [50, 10], "occupier": "Jonas und Robin"},
            {'name': 'MW-2', 'location': [51, 9], "occupier": "Jonas und Robin"},
            {'name': 'MI-1', 'location': [50, 9], "occupier": "Jonas und Robin"},
            {'name': 'MI-2', 'location': [51, 10], "occupier": "Jonas und Robin"}]


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
