#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-22"
__version__ = "0.0.1"

__all__ = ('LectureHall',)

from apis.v1.database import db


class LectureHall(db.Document):
    name = db.StringField()
    ident = db.StringField()
    test = db.StringField()


if __name__ == '__main__': pass
