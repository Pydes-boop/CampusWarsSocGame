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
from typing import Union, Optional, Iterable, DefaultDict, Dict, Set

MULTIPLIER_MAX: int = 2
MULTIPLIER_INCREASE: float = 0.02
MW_INTERVAL: int = 60


@dataclass
class Room:
    room: str
    team: str
    multiplier: float

    def __init__(self, team: str, room: str):
        self.team = team
        self.room = room
        self.multiplier = 1.0

    def reset(self) -> None:
        self.multiplier = 1

    def increase(self) -> float:
        self.multiplier = max(1.0, min(self.multiplier + MULTIPLIER_INCREASE, MULTIPLIER_MAX))
        return self.multiplier


class MultiplierWatchdog(dict, Dict[str, Room]):
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
    def __init__(self):
        super(Teams, self).__init__(Rooms)


class TeamState:
    teams: Teams
    mw: MultiplierWatchdog

    __slots__ = ('teams', 'mw',)

    def __init__(self, teams: Teams = None):
        self.teams = teams or Teams()
        self.mw = MultiplierWatchdog(self)
        self.mw.start()

    def __call__(self, team: str) -> None:
        """Create an empty team. Probably useless but it is here."""
        self.teams[team]

    def get_team_score_of_room(self, team: str, room: str) -> int:
        """Get what score a team has in a certain room."""
        return self.teams[team][room]

    def get_all_team_scores_in_room(self, room: str) -> Dict[str, int]:
        """"""
        return dict((name, team[room]) for name, team in self.teams.items())

    def get_all_teams_for_all_rooms(self) -> Dict[str, Dict[str, int]]:
        return dict((room, self.get_all_team_scores_in_room(room)) for room in self.get_rooms())

    def get_occupiers_for_all_rooms(self) -> Dict[str, str]:
        return dict((room, self.get_room_occupier(room)) for room in self.get_rooms())

    def get_room_occupier(self, room: str) -> Optional[str]:
        """Get the team that occupies a certain room."""
        all_team_scores = dict(zip(self.teams.keys(), map(itemgetter(room), self.teams.values())))
        m = max(all_team_scores.values())
        teams = [key for key, value in all_team_scores.items() if value == m]
        if not teams: return None
        if len(teams) > 1 and room in self.mw: return self.mw[room].team
        return teams[0]

    def get_rooms(self) -> Set[str]:
        rooms = set()
        for room in self.teams.values():
            rooms.update(room.keys())
        return rooms

    def is_occupier(self, team: str, room: str) -> bool:
        """Is a team the occupier of a room."""
        return team in self.get_room_occupier(room)

    def increase_team_presence_in_room(self, team: str, room: str, value: int = 1) -> None:
        """It does what it says."""
        self.teams[team].increase(room, value)

    def decrease_team_presence_in_room(self, team: str, room: str, value: int = 1) -> None:
        """It does what it says."""
        self.teams[team].decrease(room, value)

    def save(self, path: Union[Path, str]) -> None:
        """Save a compressed version to a file."""
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
    # tm = TeamState.from_load('test.mem')
    # tm = TeamState()
    # tm('TrustworthyZebras')
    # tm('BraveSquirrels')
    # tm['TrustworthyZebras']['MI-1']
    # tm['TrustworthyZebras']['MI-2']
    # tm['BraveSquirrels']['MI-1']
    # tm['BraveSquirrels']['MI-2']
    # tm.increase_team_presence_in_room('BraveSquirrels', 'MI-2', 30)
    # tm.increase_team_presence_in_room('TrustworthyZebras', 'MI-2', 30)
    # print(tm)
    # tm.save('test.mem')
    # print(compress(dumps(tm)))

    # tm = TeamState()
    # tm('TrustworthyZebras')
    # tm('BraveSquirrels')
    # tm['TrustworthyZebras']['MI-1']
    # tm['TrustworthyZebras']['MI-2']
    # tm['BraveSquirrels']['MI-1']
    # tm['BraveSquirrels']['MI-2']
    #
    # tm.increase_team_presence_in_room('BraveSquirrels', 'MI-2', 30)
    # tm.increase_team_presence_in_room('TrustworthyZebras', 'MI-2', 30)
    # print(tm.get_room_occupier('MI-2'))
    # tm.decrease_team_presence_in_room('BraveSquirrels', 'MI-2')
    # print(tm.get_room_occupier('MI-2'))
    # # print(tm)
