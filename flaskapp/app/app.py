#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-05-13"
__version__ = "0.0.1"

__all__ = ('create_app',)

from os import environ
from config import DevelopmentConfig
from flask import Flask, jsonify
from apis.v1.routes import v1
from apis.v1 import mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    # app.register_blueprint(v1)  # TODO update if necessary
    app.register_blueprint(v1, url_prefix='/v1')

    app.config["MONGO_URI"] = 'mongodb://' + environ['MONGODB_USERNAME'] + ':' \
                              + environ['MONGODB_PASSWORD'] + '@' \
                              + environ['MONGODB_HOSTNAME'] + ':27017/' + environ['MONGODB_DATABASE']
    mongo.init_app(app)

    @app.after_request
    def header(response):
        response.headers['Server'] = 'CampusWarsBackend/0.0.1'
        response.headers['X-Robots-Tag'] = 'noindex, noarchive'
        response.headers['Accept'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    return app


if __name__ == "__main__":
    application = create_app()
    ENVIRONMENT_DEBUG = environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
