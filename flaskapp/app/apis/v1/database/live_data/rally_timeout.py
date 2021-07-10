#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('RallyTimeout',)


from apis.v1.database.live_data.timed_queue import TimedQueue
from apis.v1.database.live_data.items import RallyItem
from operator import attrgetter
from typing import Optional, Dict


class RallyTimeout(TimedQueue):
    life_time = 1_800
    max_refresh = 0

    def __call__(self, team: str, room: str, name: str) -> bool:
        """Add team."""
        if team in self: return False
        self[team] = RallyItem(team, room, name)
        return True

    # def __contains__(self, team: str) -> True:
    #     return team in map(attrgetter('team'), self.values())

    def info(self, team: str) -> Optional[Dict[str, str]]:
        """Get data for frontend."""
        try:
            item = self[team]
            return dict(name=item.initiator, room=item.room)
        except ValueError:
            return None


if __name__ == '__main__': pass
