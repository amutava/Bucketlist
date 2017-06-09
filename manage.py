import os
import unittest

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api


from application import create_app, db
from application.api.models import BucketList, BucketListItems
from application.auth.models import User

app = create_app(os.getenv('BUCKETLIST_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


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

@manager.command
def test():
    """Method to run tests automatically."""
    tests = unittest.TestLoader().discover('./application/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
if __name__ == '__main__':
    manager.run()
