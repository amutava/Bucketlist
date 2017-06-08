import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

from app import create_app, db
from app.api.models import BucketList, BucketListItems
from app.auth.models import User
from app.api.controller import BucketLists, BucketListItem, SingleBucketList, SingleBucketListItem
from app.auth.controller import Register, Login

app = create_app(os.getenv('BUCKETLIST_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
api = Api(app)

def make_shell_context():
    """Returns application and database instances
    to the shell importing them automatically on
    python manage.py shell.
    """
    return dict(app=app,
                db=db,
                User=User,
                BucketList=BucketList,
                BucketListItems=BucketListItems,
                SingleBucketList=SingleBucketList,
                SingleBucketListItem=SingleBucketListItem)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(BucketLists, '/bucketlists')
api.add_resource(SingleBucketList, '/bucketlists/<bucketlist_id>')
api.add_resource(BucketListItem, '/bucketlistitems/<bucketlist_id>/items')
api.add_resource(SingleBucketListItem,
                 '/bucketlistitems/<bucketlist_id>/items/<item_id>')

if __name__ == '__main__':
    manager.run()
