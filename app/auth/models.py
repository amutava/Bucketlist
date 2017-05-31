import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import g


from app import db
from . import mod_auth



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    # @auth.verify_password
    # def verify_password(username_or_token, password):
    # # first try to authenticate by token
    #     user = User.verify_auth_token(username_or_token)
    #     if not user:
    #         # try to authenticate with username/password
    #         user = User.query.filter_by(username=username_or_token).first()
    #         if not user or not user.verify_password(password):
    #             return False
    #     g.user = user
    #     return True          
