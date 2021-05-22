#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('app',)

from flask import Flask
from apis.v1.routes import v1
from apis.v1 import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    # app.register_blueprint(v1)  # TODO update if necessary
    app.register_blueprint(v1, url_prefix='/v1')

    app.config['MONGODB_SETTINGS'] = dict(
        db='DB',  # TODO
        host='URI',  # TODO
        port=2701  # TODO maybe?
    )
    db.init_app(app)

    @app.after_request
    def header(response):
        # TODO @Felix add the other options you use, some are probably the same by default though
        response.headers['Server'] = 'CampusWarsBackend/0.0.1'
        response.headers['X-Robots-Tag'] = 'noindex, noarchive'
        response.headers['Accept'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    return app


if __name__ == '__main__':
    create_app()
