#!/usr/bin/python
# -*- coding: utf-8 -*-

__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('UID', 'User', 'Team', 'Game', 'RallyItem',)

from dataclasses import dataclass
from operator import attrgetter
from typing import Any, Union, Optional, List, Dict


@dataclass
class UID:
    uid: str

    @property
    def json(self) -> Dict[str, str]:
        return dict(uid=self.uid)


@dataclass(init=False)
class User(UID):
    team: str
    room: str

    def __init__(self, uid: str, team: str, room: str):
        self.uid = uid
        self.team = team
        self.room = room

    @property
    def json(self) -> Dict[str, str]:
        return dict(uid=self.uid, team=self.team, room=self.room)


@dataclass
class Team:
    team: str
    multiplier: float

    @property
    def json(self) -> Dict[str, Union[str, float]]:
        return dict(team=self.team, multiplier=self.multiplier)


@dataclass
class Game:
    game_id: str
    players: List[User]
    results: List[int]
    finished: List[bool]
    quiz_name: Optional[str]
    question: Optional[Dict[str, Any]]

    def __init__(self, game_id: str, players: List[User], quiz_name: str, question: Dict[str, Any]):
        self.game_id = game_id
        self.players = players
        self.results = [-2, -2]
        self.finished = [False, False]
        self.quiz_name = quiz_name
        self.question = question

    def player_in_game(self, uid: str) -> bool:
        return uid in map(attrgetter('uid'), self.players)

    @property
    def is_finished(self) -> bool:
        return all(self.finished)

    def set_finished(self, pid: int, state: bool = True) -> None:
        self.finished[pid] = state

    @property
    def all_answered(self) -> bool:
        return sum(self.results) >= 0

    def answer(self, pid: int, answer: int) -> None:
        self.results[pid] = answer

    def get_player_id(self, uid: str) -> int:
        return list(map(attrgetter('uid'), self.players)).index(uid)

    def get_result_for_player(self, pid: int) -> str:
        # we might treat a 'both won' scenario differently that a 'both lost' one, but for now they are the same
        if self.results[pid] == self.results[not pid]:
            return 'TIE'
        if self.results[pid] and not self.results[not pid]:
            return 'WON'
        else:
            return 'LOST'

    @property
    def json(self) -> Dict[str, Union[str, List[int], List[User]]]:
        return dict(
            gid=self.game_id,
            players={0: self.players[0].json, 1: self.players[1].json},
            quiz_name=self.quiz_name,
            quiz=self.question,
            results=self.results,
            finished=self.finished,
        )


@dataclass
class RallyItem:
    team: str
    room: str
    initiator: str

    @property
    def json(self) -> Dict[str, str]:
        return dict(team=self.team, room=self.room, initiator=self.initiator)


if __name__ == '__main__': pass
