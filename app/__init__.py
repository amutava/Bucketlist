import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from instance.config import config


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    return app
