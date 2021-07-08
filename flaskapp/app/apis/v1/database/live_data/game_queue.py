#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('GameQueue', 'create_game_id',)

from apis.v1.database.live_data.timed_queue import TimedQueue
from apis.v1.database.live_data.items import Game
from os import urandom
from base64 import b64encode
from typing import Optional


def create_game_id(length: int = 24) -> str:
    return b64encode(urandom(length)).decode('utf-8')


class GameQueue(TimedQueue):
    life_time = 300
    max_refresh = 350

    def __call__(self, gid: str) -> None:
        if gid in self:
            self.refresh(gid)

    def is_player_in_game(self, uid: str) -> Optional[Game]:
        for game in self.values():
            if game.player_in_game(uid):
                return game
        return None

    def submit_answer(self, gid: str, pid: int, answer: int) -> None:
        self[gid].results[pid] = answer

    def close(self, gid: str) -> None:
        del self[gid]


if __name__ == '__main__': pass
