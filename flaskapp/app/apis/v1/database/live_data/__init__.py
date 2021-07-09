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
from typing import Any, Dict


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
    def json(self) -> Dict[str, Any]:
        return dict(
            room_queue=dict(self.room_queue.debug_items()),
            quiz_queue=dict(self.quiz_queue.debug_items()),
            game_queue=dict(self.game_queue.debug_items()),
            timedout_users=dict(self.timedout_users.debug_items()),
            rally_timeout=dict(self.rally_timeout.debug_items()),
            misc=dict(
                multiplier_max_occupancy=self.room_queue.multiplier.max_occupancy,
                multiplier=self.room_queue.multiplier,
                room_queue_counter=self.room_queue.counter,
                room_queue_values=self.room_queue.values()
            )
        )


if __name__ == '__main__': pass
