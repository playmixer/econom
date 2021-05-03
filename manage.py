from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from core.database import db
from main import create_app
from apps.auth.models import User
from apps.auth.auth import Auth

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

@manager.command
def createuser(username, password):
    user = Auth.registration(username, password)
    if user:
        print(f'User {user.username} created')
        return

    print('User create failed')
    return


if __name__ == "__main__":
    manager.run()
