#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-06-27"
__version__ = "0.0.1"

__all__ = ('live_data', 'team_state',)

from apis.v1.database.team_state import TeamState
from apis.v1.database.live_data import LiveData

team_state: TeamState = TeamState()
live_data: LiveData = LiveData(team_state)

if __name__ == '__main__': pass
