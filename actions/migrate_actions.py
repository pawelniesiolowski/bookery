from flask_script import Command
import csv
import json
from decimal import Decimal
from datetime import datetime
from app.bookaction.models import BookAction, BookActionName
from app.catalog.models import Book
from app.receiver.models import Receiver
from sqlalchemy.orm.exc import NoResultFound


class ActionsMigrator(Command):
    def run(self):
        with open('data/book_change_event.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = self.prepare_name(row['name'])
                    inserted_at = self.prepare_inserted_at(row['date'])
                    copies = int(row['num'])
                    comment = None if row['comment'] == 'NULL' else row['comment']
                    book_id = self.prepare_book_id(row['book_title'])
                    receiver_id = self.prepare_receiver_id(name, row['receiver_name'])
                    action = BookAction(
                        name,
                        copies,
                        book_id=book_id,
                        receiver_id=receiver_id,
                        comment=comment
                    )
                    action.inserted_at = inserted_at
                    action.save()
                except NoResultFound:
                    continue
                print(f'Inserted action: {action}')

    def prepare_name(self, name):
        if name == 'Receive':
            return BookActionName.RECEIVE
        elif name == 'Release':
            return BookActionName.RELEASE
        elif name == 'Sell':
            return BookActionName.SELL
        else:
            raise ValueError(f'Invalid book action name: {name}')

    def prepare_book_id(self, title):
        return Book.query.filter(Book.title == title, Book.deleted_at == None).one().id

    def prepare_receiver_id(self, action_name, receiver_name):
        if action_name != BookActionName.RELEASE:
            return None
        else:
            receiver_name = receiver_name.split()
            return Receiver.query.filter(Receiver.name == receiver_name[1], Receiver.surname == receiver_name[0]).one().id



    def prepare_inserted_at(self, inserted_at):
        return datetime.fromisoformat(inserted_at)
