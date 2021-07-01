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
from abc import ABCMeta, abstractmethod
from os import urandom
from base64 import b64encode
from apis.v1.database.team_state import TeamState
from apis.v1.database.interface import get_current_quizzes, get_questions_of_quiz
from operator import attrgetter
from random import choice
from bson import ObjectId

from typing import Any, Union, Optional, Dict, List, Tuple

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
    refresh_max = REFRESH_MAX_USER

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
    readiness: List[bool]

    def __init__(self, game_id: str, players: List[User], question: Dict[str, Any]):
        self.game_id = game_id
        self.players = players
        self.results = [-2, -2]
        self.question = question
        self.readiness = [False, False]

    def player_in_game(self, uid: str) -> bool:
        return uid in map(attrgetter('uid'), self.players)

    @property
    def ready(self) -> bool:
        return all(self.readiness)

    def set_ready(self, uid: str, state: bool = True) -> None:
        self.readiness[self.get_player_id(uid)] = state

    @property
    def all_answered(self) -> bool:
        return sum(self.results) >= 0

    def answer(self, pid: int, answer: int):
        self.results[pid] = answer

    def get_player_id(self, uid: str) -> int:
        return list(map(attrgetter('uid'), self.players)).index(uid)

    def get_result_for_player(self, pid: int) -> str:
        if self.results[pid] and not self.results[not pid]:
            return 'WON'
        if self.results[pid] and self.results[not pid]:
            return 'TIE'
        else:
            return 'LOST'

    @property
    def json(self):
        return self.__dict__


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

    def __init__(self):
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
    team_data: TeamState

    def __init__(self, team_data: Optional[TeamState]):
        self.team_data = team_data
        super(RoomQueue, self).__init__()

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
                if self.team_data: self.team_data.decrease_team_presence_in_room(team=user.team, room=user.room)
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
    game_queue: 'GameQueue'

    def __init__(self, game_queue: 'GameQueue'):
        self.game_queue = game_queue
        super(QuizQueue, self).__init__(None)

    def __call__(self, uid: str, team: str, room: str, lid: str = None) -> Optional[Tuple[str, Union[Game]]]:
        """Do everything at once really..."""
        if uid in self:
            game = self.game_queue.is_player_in_game(uid)
            if game:  # player was added to a game before
                del self[uid]
                return 'game', game

            if uid in self and room == self[uid].room == room:  # player adds another into a game
                opp = self.get_opponent(self[uid])
                if opp:
                    game = Game(game_id=game_id(),
                                players=[self[uid], opp],
                                question=choice(get_questions_of_quiz((get_current_quizzes(ObjectId(lid))[0]["_id"])))
                                # question=choice(get_questions_of_quiz(choice(get_current_quizzes(ObjectId(lid)))))
                    )  # TODO
                    del self[uid], self[opp.uid]
                    self.game_queue[game.game_id] = game
                    return 'game-incomplete', game

            self[uid].refresh()  # just a state refresh from a player that still wants to play
        else:
            self[uid] = User(uid, future(), team, room)  # a new player wants to join a game

    def get_opponent(self, user: User) -> Optional[User]:
        values = self.values()
        shuffle(list(values))
        for opp in values:
            if opp.room == user.room and opp.team != user.team and not opp.freed:
                return opp
        else:
            return None


class GameQueue(PurgeQueue):
    def __call__(self, players, question):
        gid = game_id()
        self[gid] = Game(gid, players, question)

    def is_player_in_game(self, uid: str) -> Optional[Game]:
        for game in self.values():
            if game.player_in_game(uid):
                return game
        else:
            return None

    def submit_answer(self, gid: str, pid: str, answer: int) -> None:
        self[gid].results[pid] = answer

    def close(self, gid: str):
        del self[gid]

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


class LiveData:
    room_queue: RoomQueue
    quiz_queue: QuizQueue
    game_queue: GameQueue

    def __init__(self, team_state: TeamState):
        self.room_queue = RoomQueue(team_state)
        self.game_queue = GameQueue()
        self.quiz_queue = QuizQueue(self.game_queue)


if __name__ == '__main__':
    game = Game('123',
                [
                    User('1234', 123, 'team1', 'MW-1'),
                    User('124', 123, 'team2', 'MW-1')],
                {}
                )
    print(game.get_player_id('124'))
