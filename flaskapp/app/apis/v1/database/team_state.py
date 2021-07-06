#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-24"
__version__ = "0.0.1"

__all__ = ('TeamState',)

from pathlib import Path
from operator import itemgetter
from collections import defaultdict
from gzip import compress, decompress
from pickle import dumps, loads
from threading import Thread
from time import sleep
from dataclasses import dataclass
from typing import Union, Optional, DefaultDict, Dict, Set

MULTIPLIER_MAX: int = 2
MULTIPLIER_INCREASE: float = 0.005
MW_INTERVAL: int = 5


@dataclass
class Room:
    """Stores the current occupier in a room."""
    room: str
    team: str
    multiplier: float

    def __init__(self, team: str, room: str):
        self.team = team
        self.room = room
        self.multiplier = 1.0

    def reset(self) -> None:
        """Reset room multiplier when occupier changes"""
        self.multiplier = 1

    def increase(self) -> float:
        """Increase the occupiers multiplier."""
        self.multiplier = max(1.0, min(self.multiplier + MULTIPLIER_INCREASE, MULTIPLIER_MAX))
        return self.multiplier


class MultiplierWatchdog(dict, Dict[str, Room]):
    """Manage the occupier for each room."""

    thread: Thread
    running: bool
    current_interval: int

    team_state: 'TeamState'
    occupiers: Dict[str, Room]

    def __init__(self, team_state: 'TeamState'):
        self.thread = Thread(name='Multiplayerwatchdog', target=self.run)
        self.current_interval = 0
        self.running = True
        super(MultiplierWatchdog, self).__init__()
        self.team_state = team_state
        self.mw = defaultdict(lambda: None)

    def run(self) -> None:
        while self.running:
            sleep(1)
            self.current_interval += 1
            if self.current_interval <= MW_INTERVAL:
                self.current_interval = 0
                self.check()

    def check(self) -> None:
        """Check whether the occupier multiplier has to be increased or reset."""
        for room, team in self.team_state.get_occupiers_for_all_rooms():
            if team == self[room].team:
                self[room].increase()
            else:
                self[room].team = team
                self[room].reset()

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.running = False

    def __getitem__(self, item: str) -> Room:
        try:
            return super(MultiplierWatchdog, self).__getitem__(item)
        except KeyError:
            room = Room(self.team_state.get_room_occupier(item), item)
            self[item] = room
        return room


class Rooms(defaultdict, DefaultDict[str, int]):
    """Stores all occupancy values of a team for each room."""
    def __init__(self):
        super(Rooms, self).__init__(int)

    def increase(self, room: str, value: int = 1) -> int:
        """Increase the given team score. Defaults to 1"""
        self[room] += value
        return self[room]

    def decrease(self, room: str, value: int = 1) -> int:
        """Decrease the given team score. Defaults to 1"""
        self[room] -= value
        return self[room]

    def clear_scores(self) -> None:
        """Set all scores to zero. Do NOT confuse with `clear()`!"""
        for room in self:
            self[room] = 0


class Teams(defaultdict, DefaultDict[str, Rooms]):
    """Represents all teams an their rooms."""
    def __init__(self):
        super(Teams, self).__init__(Rooms)


class TeamState:
    """General Team State Manager."""
    teams: Teams
    mw: MultiplierWatchdog

    __slots__ = ('teams', 'mw',)

    def __init__(self, teams: Teams = None):
        self.teams = teams or Teams()
        self.mw = MultiplierWatchdog(self)
        self.mw.start()

    def __call__(self, team: str) -> None:
        """Create an empty team."""
        self.teams[team]

    def get_team_occupancy_of_room(self, team: str, room: str) -> int:
        return self.teams[team][room]

    def get_all_team_occupancy_in_room(self, room: str) -> Dict[str, int]:
        return dict((name, team[room]) for name, team in self.teams.items())

    def get_all_teams_for_all_rooms(self) -> Dict[str, Dict[str, int]]:
        return dict((room, self.get_all_team_occupancy_in_room(room)) for room in self.get_all_rooms())

    def get_occupiers_for_all_rooms(self) -> Dict[str, str]:
        return dict((room, self.get_room_occupier(room)) for room in self.get_all_rooms())

    def get_room_occupier(self, room: str) -> Optional[str]:
        all_team_scores = dict(zip(self.teams.keys(), map(itemgetter(room), self.teams.values())))
        if not all_team_scores: return None
        m = max(all_team_scores.values())
        teams = [key for key, value in all_team_scores.items() if value == m]
        if not teams: return None
        if len(teams) > 1 and room in self.mw: return self.mw[room].team
        return teams[0]

    def get_all_rooms(self) -> Set[str]:
        rooms = set()
        for room in self.teams.values():
            rooms.update(room.keys())
        return rooms

    def is_occupier(self, team: str, room: str) -> bool:
        return team in self.get_room_occupier(room)

    def increase_team_presence_in_room(self, team: str, room: str, value: int = 1) -> None:
        self.teams[team].increase(room, value)

    def decrease_team_presence_in_room(self, team: str, room: str, value: int = 1) -> None:
        self.teams[team].decrease(room, value)

    def save(self, path: Union[Path, str]) -> None:
        """Save a compressed representation of the state to a file."""
        Path(path).write_bytes(compress(dumps(self.teams)))

    @classmethod
    def from_load(cls, path: Union[Path, str]) -> 'TeamState':
        """Load database from a file"""
        return cls(loads(decompress(Path(path).read_bytes())))

    def __str__(self) -> str:
        return str(self.teams)

    def __repr__(self) -> str:
        return repr(self.teams)

    def __getitem__(self, item: str) -> Rooms:
        return self.teams[item]

    def __setitem__(self, key: str, value: Rooms) -> None:
        self.teams[key] = value


if __name__ == '__main__':
    pass
