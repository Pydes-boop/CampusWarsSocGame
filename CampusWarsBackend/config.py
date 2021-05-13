#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('DevelopmentConfig', 'ProductionConfig',)

from dotenv import dotenv_values
from pathlib import Path

SECRETS_PATH: Path = Path('.secrets')
if not SECRETS_PATH.exists():
    raise FileNotFoundError(f'The file "{SECRETS_PATH}" is missing! It is not in the repository, request it!') from None
secrets = dotenv_values(SECRETS_PATH)


class Config:
    print('Config')
    DEBUG: bool = False
    TESTING: bool = False
    CSRF_ENABLED: bool = True
    SECRET_KEY: str = secrets['SECRET_KEY']


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV: str = 'development'
    DEVELOPMENT: bool = True


if __name__ == '__main__':
    pass
