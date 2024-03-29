#!/usr/bin/python
# coding=utf-8
import os

from flask import Flask
from . import db, auth, api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(
            app.instance_path, 'app.sqlite'),  # sqlite 文件保存地址
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    # a simple page that says hello
    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
