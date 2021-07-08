#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('QuizQueue',)

from apis.v1.database.live_data.timed_queue import TimedQueue
from apis.v1.database.live_data.game_queue import create_game_id
from apis.v1.database.live_data.items import User, Game
from apis.v1.database.time_functions import timestamp
from apis.v1.database.interface import get_current_quizzes, get_questions_of_quiz
from contextlib import suppress
from random import seed, choice, shuffle
from typing import Optional, Tuple
from bson import ObjectId

seed(timestamp())


class QuizQueue(TimedQueue):
    life_time = 20
    max_refresh = 40
    live_data: 'LiveData'

    def __init__(self, live_data: 'LiveData'):
        self.live_data = live_data
        super(QuizQueue, self).__init__()

    def __call__(self, uid: str, team: str, room: str, lid: str = None) -> Optional[Tuple[str, Game]]:
        if uid in self:
            game = self.live_data.game_queue.is_player_in_game(uid)

            if game:
                with suppress(KeyError): del self[uid]
                return 'game', game

            if room == self[uid].room:
                opp = self.get_opponent(self[uid])

                if opp:
                    quiz = choice(get_current_quizzes(ObjectId(lid)))
                    game = Game(
                        game_id=create_game_id(),
                        players=[self[uid], opp],
                        quiz_name=quiz['name'],
                        question=choice(get_current_quizzes(quiz['_id']))
                    )
                    del self[uid], self[opp.uid]
                    self.live_data.game_queue[game.game_id] = game
                    return 'game-incomplete', game

            self['uid'].refresh()
        else:
            self[uid] = User(uid, team, room)

    def get_opponent(self, user: User) -> Optional[User]:
        users = self.values()
        shuffle(list(users))
        for opp in users:
            if opp.room == user.room and opp.team != user.team:
                return opp
        return None


if __name__ == '__main__': pass