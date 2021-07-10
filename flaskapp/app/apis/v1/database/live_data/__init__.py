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
from contextlib import suppress
from typing import Any, Dict, Iterable


class LiveData:
    room_queue: RoomQueue
    quiz_queue: QuizQueue
    game_queue: GameQueue
    timedout_users: TimedOutUsers
    rally_timeout: RallyTimeout

    def __init__(self):
        self()

    def __call__(self, ex: Iterable[str] = None) -> None:
        ex = ex or []
        with suppress(AttributeError):
            del self.room_queue
        with suppress(AttributeError):
            del self.game_queue
        with suppress(AttributeError):
            del self.quiz_queue
        with suppress(AttributeError):
            del self.timedout_users
        with suppress(AttributeError):
            del self.rally_timeout

        if 'room' not in ex: self.room_queue = RoomQueue(self)
        if 'game' not in ex: self.game_queue = GameQueue()
        if 'quiz' not in ex: self.quiz_queue = QuizQueue(self)
        if 'timedout' not in ex: self.timedout_users = TimedOutUsers()
        if 'rally' not in ex: self.rally_timeout = RallyTimeout()

    @property
    def json(self) -> Dict[str, Any]:
        return dict(
            room_queue=dict(self.room_queue.debug_items()),
            quiz_queue=dict(self.quiz_queue.debug_items()),
            game_queue=dict(self.game_queue.debug_items()),
            timedout_users=dict(self.timedout_users.debug_items()),
            rally_timeout=dict(self.rally_timeout.debug_items()),
            # misc=dict(
            #     multiplier=self.room_queue.multiplier,
            #     room_queue_occupancy=self.room_queue.get_each_rooms_occupancies()
            # )
        )


if __name__ == '__main__': pass
