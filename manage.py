import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from actions.migrate_books import BooksMigrator
from actions.migrate_receivers import ReceiversMigrator
from actions.migrate_actions import ActionsMigrator


app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('migrate_books', BooksMigrator)
manager.add_command('migrate_receivers', ReceiversMigrator)
manager.add_command('migrate_actions', ActionsMigrator)


if __name__ == '__main__':
    from app.catalog.models import Book
    from app.receiver.models import Receiver
    from app.bookaction.models import BookAction
    from app.auth.models import User
    manager.run()
