from flask import jsonify, make_response, request

from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, Api

from app import db
from models import User


class Register(Resource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        if username is None:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Username is missing."

                         }
                         }), 400)
        if password is None:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Password is missing."

                         }
                         }), 400)

        user = User.query.filter_by(username=username).first()
        if user:
            return make_response(
                jsonify({'data': {
                    'message': "user with the username already exists.",
                    "username": username

                }}), 400)  # existing user
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return make_response(
            jsonify({'data': {
                    'message': "User registration successful.",
                    "username": username,


                    }}), 200)


class Login(Resource):

    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        if username is None:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Username is missing."

                         }
                         }), 400)
        if password is None:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Password is missing."

                         }
                         }), 400)

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            token = user.generate_auth_token(user.id)
            if token:
                return make_response(jsonify({'data': {
                    "message": "Login successful.",
                    "username": user.username,
                    "token": token.decode()
                }
                }), 200)
        return make_response(
            jsonify({'data':
                     {
                         'message': "Invalid username/password."

                     }
                     }), 400)
