#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('RoomQueue',)

from apscheduler.schedulers.background import BackgroundScheduler
from collections import defaultdict
from apis.v1.database.live_data.items import User, Team
from apis.v1.database.live_data.timed_queue import TimedQueue
from typing import Any, List, Dict

MULTIPLIER_INCREASE: float = 0.005
MULTIPLIER_UPDATE_RATE_SEC: int = 5


class Multiplier(dict, Dict[str, 'Team']):
    scheduler: BackgroundScheduler
    queue: Any

    def __init__(self, queue: Any):
        super(Multiplier, self).__init__()
        # self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Vienna'})
        # self.scheduler.start()
        # self.scheduler.add_job(self.check, 'interval', id='multiplier_check', seconds=MULTIPLIER_UPDATE_RATE_SEC)
        self.queue = queue

    def check(self) -> None:
        """Check for the current occupiers."""
        for room, teams in self.queue.get_each_rooms_occupancies().items():
            if room not in self: self[room] = Team('', 0)
            max_occupancy = max(teams.values())
            teams = [key for key, value in teams.items() if value == max_occupancy]
            if self[room].team in teams:
                self[room].multiplier += MULTIPLIER_INCREASE
            else:
                team = (teams + [''])[0]  # append empty string in case there is no occupier
                self[room].team = team
                self[room].multiplier = 1.0


class RoomQueue(TimedQueue):
    multiplier: Multiplier
    life_time = 20
    max_refresh = 40

    def __init__(self):
        super(RoomQueue, self).__init__()
        self.multiplier = Multiplier(self)

    def __call__(self, uid: str, team: str, room: str) -> None:
        """Add new user or refresh existing one."""
        if uid in self and room == self[uid].room == room:
            self.refresh(uid)
        else:
            self[uid] = User(uid, team, room)
        self.multiplier.check()

    def get_users_in_room(self, room: str) -> List[User]:
        """Get all users that are in a room."""
        return [user for user in self.values() if user.room == room]

    def get_users_in_room_from_team(self, room: str, team) -> List[User]:
        """Get all users that are in a room."""
        return [user for user in self.get_users_in_room(room) if user.team == team]

    def get_each_rooms_occupancies(self) -> Dict[str, Dict[str, int]]:
        """Get a dict of all rooms and another dict with each time and their occupancy."""
        occupancy = defaultdict(lambda: defaultdict(int))
        for user in self.values():
            occupancy[user.room][user.team] += 1
        return occupancy

    def get_each_rooms_occupiers(self) -> Dict[str, Team]:
        """Get a dict of all rooms an their current occupiers."""
        return self.multiplier


if __name__ == '__main__': pass
