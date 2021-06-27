#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-25"
__version__ = "0.0.1"

__all__ = ('RoomQueue',)

from datetime import datetime
from dataclasses import dataclass
from random import shuffle
from threading import Thread
from time import sleep
from abc import ABCMeta, abstractmethod
from os import urandom
from base64 import b64encode

from typing import Any, Optional, Dict, List

LIFE_TIME_USER: int = 20
REFRESH_MAX_USER: int = 40

LIFE_TIME_GAME: int = 600
REFRESH_MAX_GAME: int = 720

PURGE_WAIT: int = 150

now = lambda: int(datetime.now().timestamp())
future = lambda: now() + LIFE_TIME_USER * 60

game_id = lambda: b64encode(urandom(24)).decode('utf-8')


class TimedItem:
    time: int
    freed: bool = False
    life_time: int
    refresh_max: int

    def refresh(self):
        """Add time to a items lifetime."""
        # if a user adds time more often somehow, we ignore it
        if self.freed: return
        if self.time + self.life_time > now() + self.refresh_max: return
        self.time += self.life_time

    def free(self):
        """Item is to be purged on next collection."""
        self.freed = True
        self.time = 0


@dataclass
class User(TimedItem):
    life_time = LIFE_TIME_USER
    REFRESH_MAX_USER = REFRESH_MAX_USER

    uid: str
    time: int
    team: str
    room: str


class Game(TimedItem):
    life_time = LIFE_TIME_GAME
    refresh_max = REFRESH_MAX_GAME

    game_id: str
    players: List[User]
    results: List[int]
    Question: Optional[Dict[str, Any]]

    def __init__(self, game_id: str, players: List[User], question: Dict[str, Any]):
        self.game_id = game_id
        self.players = players
        self.question = question

    @property
    def ready(self):
        return len(self.players) == 2

    def answer(self, pid: int, answer: str):
        pass  # TODO ask Marina how the questions look exactly


class TheGreatPurge(Thread):
    running: bool
    data: 'PurgeQueue'

    def __init__(self, data: 'PurgeQueue'):
        self.running = True
        self.data = data
        super(TheGreatPurge, self).__init__(
            name='TheGreatPurge'
        )

    def stop(self):
        self.running = False

    def run(self) -> None:
        while self.running:
            sleep(PURGE_WAIT)
            self.data.purge()


class PurgeQueue(dict, Dict[str, Any], metaclass=ABCMeta):
    purge_thread: TheGreatPurge

    def __init__(self, ):
        self.purge_thread = TheGreatPurge(self)
        super(PurgeQueue, self).__init__()
        self.purge_thread.start()

    @abstractmethod
    def purge(self) -> int:
        """Delete timed out users."""
        pass

    def __del__(self):
        self.purge_thread.stop()


class RoomQueue(PurgeQueue):
    def __call__(self, uid: str, team: str, room: str) -> None:
        """Add new user."""
        if uid in self and room == self[uid].room == room:
            self[uid].refresh()
        else:
            self[uid] = User(uid, future(), team, room)

    def purge(self) -> int:
        """Delete invalid users."""
        count: int = 0
        time = now()
        purge_list = list()
        for uid, user, in self.items():
            if user.time < time:
                purge_list.append(uid)
                count += 1
        for uid in purge_list: del self[uid]
        return count

    def get_users_in_room(self, room: str) -> List[User]:
        """Get all users that are in a room."""
        return [user for user in self.values() if user.room == room]

    def get_users_in_room_from_team(self, room: str, team) -> List[User]:
        """Get all users that are in a room."""
        return [user for user in self.get_users_in_room(room) if user.team == team]

    def get_random_users_in_room_from_other_team(self, room: str, team: str, number_of_players: int) -> Optional[List[User]]:
        """Get a certain number of randomly selected players in a room."""
        users = self.get_users_in_room_from_team(room, team)
        shuffle(users)
        if len(users) < number_of_players: return None
        return [users.pop() for _ in users]


class QuizQueue(RoomQueue):
    pass


class GameQueue(PurgeQueue):
    def __call__(self, players, question):
        gid = game_id()
        self[gid] = Game(gid, players, question)

    def purge(self) -> int:
        count: int = 0
        time = now()
        purge_list = list()
        for gid, game, in self.items():
            if game.time < time:
                purge_list.append(gid)
                count += 1
        for gid in purge_list: del self[gid]
        return count


if __name__ == '__main__':
    pass
