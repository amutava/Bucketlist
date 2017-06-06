from flask import jsonify, abort, url_for, g, request
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, Api

from models import User



#auth = HTTPTokenAuth('Bearer')


class Register(Resource):
    def post(self):
        data = request.data
        username = data["usename"]
        password = data["password"]
        if username is None or password is None:
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400, {
                "error": {
                    "message": "User already registered."
                }
            })  # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return (jsonify({'username': user.username,
                         "message": "User registration successful."}), 201)


class Login(Resource):

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None:
            abort(400, {
                "error": {
                    "message": "Username is missing."
                }
            })
        if password is None:
            abort(400, {
                "error": {
                    "message": "Password is missing."
                }
            })

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            token = User.generate_auth_token(User.id)
            return jsonify({
                "message": "Login successful.",
                "username": user.username,
                "token": token
            })
        abort(400, {
            "error": {
                "message": "Invalid username/ password."
            }
        })