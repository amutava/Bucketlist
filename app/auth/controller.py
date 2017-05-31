from flask import jsonify, abort, url_for, g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPTokenAuth

from models import User

jwt = JWT(app.config['SECRET_KEY'], expires_in=3600)
auth = HTTPTokenAuth('Bearer')


@mod_auth.route("/auth/register/")
def register():
    pass


@mod_auth.route("/auth/login/", methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})



@mod_auth.route('/auth/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@mod_auth.route('/auth/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(3600)
    return jsonify({'token': token.decode('ascii'), 'duration': 3600})


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False
