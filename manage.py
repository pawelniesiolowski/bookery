import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db


app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    from app.catalog.book_model import Book
    from app.receiver.receiver_model import Receiver
    from app.bookaction.book_action_model import BookAction
    manager.run()
