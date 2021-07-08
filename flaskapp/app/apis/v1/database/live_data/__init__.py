#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('LiveData',)


from apis.v1.database.live_data.room_queue import RoomQueue
from apis.v1.database.live_data.quiz_queue import QuizQueue
from apis.v1.database.live_data.game_queue import GameQueue
from apis.v1.database.live_data.timedout_users import TimedOutUsers
from apis.v1.database.live_data.rally_timeout import RallyTimeout
from operator import attrgetter


class LiveData:
    room_queue: RoomQueue
    quiz_queue: QuizQueue
    game_queue: GameQueue
    timedout_users: TimedOutUsers
    rally_timeout: RallyTimeout

    def __init__(self):
        self.room_queue = RoomQueue(self)
        self.game_queue = GameQueue()
        self.quiz_queue = QuizQueue(self)
        self.timedout_users = TimedOutUsers()
        self.rally_timeout = RallyTimeout()

    @property
    def json(self):
        return [
            # self.room_queue,
            list(map(lambda x, x.self.room_queue.values()))
            self.quiz_queue,
            dict([(key, item.json) for key, item in self.game_queue.items()]),
            self.timedout_users,
            list(map(attrgetter('json'), self.rally_timeout))
        ]


if __name__ == '__main__': pass
