from app import db
from .. auth.models import User


class BucketList(db.Model):
    __tablename__ = "bucketlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description =  db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DATETIME, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))


    def __init__(self, name, description, created_by):
        self.name = name
        self.description = description
        self.created_by = created_by


class BucketListItems(db.Model):
    __tablename__ = "bucketlistitems"       
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DATETIME, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))
    done = db.Column(db.Boolean, default=False)


    def __init__(self, name, bucketlist_id, done=None):
        self.name = name
        self.done = done
        self.bucketlist_id = bucketlist_id
