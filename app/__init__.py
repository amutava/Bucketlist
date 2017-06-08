import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Blueprint
from flask_login import LoginManager

from config import config


basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
login_manager = LoginManager()



login_manager.session_protection = 'None'
login_manager.login_view = 'mod_auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	app.config['SECRET_KEY'] = 'Jsa4JL*D6P;Ep<qb'
	db.init_app(app)
	login_manager.init_app(app)
	return app
