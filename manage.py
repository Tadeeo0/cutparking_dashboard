from flask_migrate import Migrate
from flask_script import Manager
from app import create_app, db
from app.models import User  # Tus modelos

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)


from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
