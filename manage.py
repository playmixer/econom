from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from core.database import db
from main import create_app

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

if __name__ == "__main__":
    manager.run()
