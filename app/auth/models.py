from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
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
