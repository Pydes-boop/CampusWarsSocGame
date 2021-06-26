#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-25"
__version__ = "0.0.1"

__all__ = ('LiveData',)

from datetime import datetime
from dataclasses import dataclass
from random import shuffle
from threading import Thread
from time import sleep

from typing import Dict, List

LIFE_TIME: int = 3
REFRESH_MAX: int = 5

PRUNE_AUTO: str = 'auto'
PRUNE_INTERVAL: str = 'interval'
PRUNE_NONE: str = 'none'

PRUNE_INTERVAL_VALUE: int = 10
PRUNE_AUTO_VALUE: int = 5

now = lambda: int(datetime.now().timestamp())
future = lambda: now() + LIFE_TIME * 60


@dataclass
class User:
    uuid: str
    time: int
    room: str

    def refresh(self):
        """Add time to a users lifetime."""
        # if a user adds time more often somehow, we ignore it
        if self.time + LIFE_TIME * 60 > now() + REFRESH_MAX * 60: return
        self.time += LIFE_TIME * 60


class TheGreatPurge(Thread):
    running: bool
    live_data: 'LiveData'

    def __init__(self, live_data: 'LiveData'):
        self.running = True
        self.live_data = live_data
        super(TheGreatPurge, self).__init__(
            name='TheGreatPurge'
        )

    def stop(self):
        self.running = False

    def run(self) -> None:
        while self.running:
            sleep(PRUNE_AUTO_VALUE * 60)
            self.live_data.prune()


class LiveData(dict, Dict[str, User]):
    prune_mode: str
    thread: Thread
    current_intervall: int

    def __init__(self, prune_mode: str = PRUNE_AUTO):
        super(LiveData, self).__init__()
        self.prune_mode = prune_mode
        if self.prune_mode == PRUNE_AUTO:
            self.thread = TheGreatPurge(self)
            self.thread.start()
        if prune_mode == PRUNE_INTERVAL:
            self.current_intervall = PRUNE_INTERVAL_VALUE

    def __call__(self, uuid: str, room: str) -> None:
        """Add new user."""
        if uuid in self and room == self[uuid].room == room:
            self[uuid].refresh()
        else:
            self[uuid] = User(uuid, future(), room)

    def __getitem__(self, item: str) -> User:
        if self.prune_mode == PRUNE_INTERVAL and self.current_intervall == 0:
            self.current_intervall = PRUNE_INTERVAL_VALUE
            self.prune()
        return super(LiveData, self).__getitem__(item)

    def __setitem__(self, key: str, value: User) -> None:
        if self.prune_mode == PRUNE_INTERVAL and self.current_intervall == 0:
            self.current_intervall = PRUNE_INTERVAL_VALUE
            self.prune()
        return super(LiveData, self).__setitem__(key, value)

    def prune(self) -> int:
        """Delete invalid users."""
        count: int = 0
        time = now()
        purge_list = list()
        for uuid, user, in self.items():
            if user.time < time:
                purge_list.append(uuid)
                count += 1
        for uuid in purge_list: del self[uuid]
        return count

    def get_users_in_room(self, room: str) -> List[User]:
        """Get all users that are in a room."""
        return [user for user in self.values() if user.room == room]

    def get_random_users_in_room(self, room: str, number_of_players: int) -> List[User]:
        """Get a certain number of randomly selected players in a room."""
        users = self.get_users_in_room(room)
        shuffle(users)
        return [users.pop() for _ in range(number_of_players)]


if __name__ == '__main__':
    pass
