import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

from config import config

db = SQLAlchemy()

from application.api.controller import (BucketLists, 
            BucketListItem, SingleBucketList, 
            SingleBucketListItem)
from application.auth.controller import Register, Login

basedir = os.path.abspath(os.path.dirname(__file__))

app_blueprint = Blueprint('api', __name__)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    api = Api(app)
    CORS(app)
    app.config['SECRET_KEY'] = 'Jsa4JL*D6P;Ep<qb'
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    api.add_resource(BucketLists, '/bucketlists')
    api.add_resource(SingleBucketList, '/bucketlists/<bucketlist_id>')
    api.add_resource(BucketListItem, '/bucketlistitems/<bucketlist_id>/items')
    api.add_resource(SingleBucketListItem,
                 '/bucketlistitems/<bucketlist_id>/items/<item_id>/')
    db.init_app(app)
    return app

app = create_app(os.getenv('BUCKETLIST_CONFIG') or 'default')