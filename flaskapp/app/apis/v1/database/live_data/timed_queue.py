#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Robin "r0w" Weiland'
__date__ = '2021-07-07'
__version__ = '0.0.1'

__all__ = ('TimedQueue',)

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
from operator import attrgetter
from dataclasses import dataclass
from contextlib import suppress
from apis.v1.database.time_functions import timestamp
from typing import Any, Dict


class TimedQueue(dict, Dict[str, 'Item']):
    scheduler: BackgroundScheduler
    life_time: int
    max_refresh: int

    @dataclass
    class Item:
        name: str
        job: Job
        item: str

        @property
        def eta(self) -> int:
            """Time the object gets 'game ended'"""
            return self.job.next_run_time.timestamp()

        @property
        def eta_debug(self):
            return str(self.job.next_run_time)

    def __init__(self):
        super(TimedQueue, self).__init__()
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Vienna'})
        self.scheduler.start()

    def __del__(self) -> None:
        self.scheduler.shutdown()

    def __getitem__(self, item: str) -> Any:
        if item not in self: return None
        return super(TimedQueue, self).__getitem__(item).item

    def __setitem__(self, key, value) -> None:
        if key not in self and not isinstance(value, TimedQueue.Item):
            self.add(key, value)
        if not isinstance(value, TimedQueue.Item):
            self[key].item = value
        else:
            super(TimedQueue, self).__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        with suppress(AttributeError): self.get(key).job.remove()
        with suppress(KeyError): super(TimedQueue, self).__delitem__(key)

    def refresh(self, item: str) -> bool:
        """Attempt to refresh the lifetime of an object."""
        item = self.get(item)
        if item.eta + self.life_time > timestamp() + self.max_refresh: return False
        item.job.reschedule('interval', seconds=item.eta + self.life_time)
        return True

    def eta(self, item: str) -> int:
        return self.get(item).eta

    def add(self, name: str, item: Any) -> bool:
        if name in self: return self.refresh(item)
        self[name] = TimedQueue.Item(
            name,
            self.scheduler.add_job(self.__delitem__,
                                   'interval',
                                   args=(name,),
                                   id=f'{self.__class__.__name__}:{name}',
                                   seconds=self.life_time),
            item
        )

    def dict(self):
        """Get a 'normal' representation of the dict."""
        return dict(zip(self.keys(), map(attrgetter('item'), self.values())))

    def values(self):
        return map(attrgetter('item'), super().values())

    def debug_values(self):
        for item in self:
            r = self[item].__dict__
            r.update(dict(time=self.get(item).eta_debug))
            yield r

    def items(self):
        return zip(self.keys(), self.values())


if __name__ == '__main__': pass
