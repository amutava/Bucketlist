from app import db


class BucketList(db.Model):
    id = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.Integer, primary_key=True)
    description =  db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DATETIME, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
