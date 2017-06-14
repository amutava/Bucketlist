from flask import jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, Api

from application import db
from application.auth.models import User


class Register(Resource):
    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
            if not username:
                return make_response(
                    jsonify(
                        {
                            'message': "Username is missing."

                        }
                    ), 400)
            if not password:
                return make_response(
                    jsonify(
                        {
                            'message': "Password is missing."

                        }
                    ), 400)
            user = User.query.filter_by(username=username).first()
            if user:
                return make_response(
                    jsonify({
                        'message': "User with the username already exists.",
                        "username": username

                    }), 409)  # existing user
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return make_response(
                jsonify({
                    'message': "User registration successful.",
                    "username": username,


                }), 200)
        except:
            return make_response(jsonify({
                "error": "missing data in request."
            }), 404)


class Login(Resource):

    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
            if not username:
                return make_response(
                    jsonify(
                        {
                            'message': "Username is missing."

                        }
                    ), 400)
            if not password:
                return make_response(
                    jsonify(
                        {
                            'message': "Password is missing."

                        }
                    ), 400)

            user = User.query.filter_by(username=username).first()
            if user and user.verify_password(password):
                token = user.generate_auth_token(user.id)
                if token:
                    return make_response(jsonify( {
                        "message": "Login successful.",
                        "username": user.username,
                        "token": token.decode()
                    }
                    ), 200)
            return make_response(
                jsonify(
                         {
                             'message': "Invalid username/password."

                         }
                         ), 401)
        except:
            return make_response(jsonify({
                "error": "missing data in request."
            }), 404)    
