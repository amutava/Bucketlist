import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from instance.config import config


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from auth import mod_auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    return app
