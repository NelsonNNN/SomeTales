import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from tales import create_app, db

app=create_app()

with app.app_context():

    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()