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
from typing import Union, Iterable, DefaultDict


class Rooms(defaultdict, DefaultDict[str, int]):
    def __init__(self):
        super(Rooms, self).__init__(int)

    def increase(self, room: str, value: int = 1) -> None:
        """Increase the given team score. Defaults to 1"""
        self[room] += value

    def decrease(self, room: str, value: int = 1) -> None:
        """Decrease the given team score. Defaults to 1"""
        self[room] -= value

    def clear_scores(self) -> None:
        """Set all scores to zero. Do NOT confuse with `clear()`!"""
        for room in self:
            self[room] = 0


class Teams(defaultdict, DefaultDict[str, Rooms]):
    def __init__(self):
        super(Teams, self).__init__(Rooms)


class TeamState:
    teams: Teams

    __slots__ = ('teams',)

    def __init__(self, teams: Teams = None):
        self.teams = teams or Teams()

    def __call__(self, team: str) -> None:
        """Create an empty team. Probably useless but it is here."""
        self.teams[team]

    def get_team_score_of_room(self, team: str, room: str) -> int:
        """Get what score a team has in a certain room."""
        return self.teams[team][room]

    def get_room_occupier(self, room: str) -> Iterable[str]:
        """Get the team that occupies a certain room."""
        all_team_scores = dict(zip(self.teams.keys(), map(itemgetter(room), self.teams.values())))
        m = max(all_team_scores.values())
        return [key for key, value in all_team_scores.items() if value == m]

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
