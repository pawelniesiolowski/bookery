from .. import db
from datetime import datetime
from sqlalchemy.orm import validates
from enum import Enum


class BookActionName(Enum):
    RECEIVE = 1
    RELEASE = 2
    SELL = 3


class BookAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(BookActionName), nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    inserted_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, copies, *, book_id, receiver_id=None, **kwargs):
        super(BookAction, self).__init__(**kwargs)
        self.name = name
        self.copies = copies
        self.book_id = book_id
        self.receiver_id = receiver_id
        self.inserted_at = datetime.now()

    @validates('name')
    def validate_name(self, key, value):
        assert value and isinstance(value, BookActionName)
        return value

    @validates('copies')
    def validate_copies(self, key, value):
        self.validate_number(value)
        return value

    @validates('book_id')
    def validate_book_id(self, key, value):
        self.validate_number(value)
        return value

    @validates('receiver_id')
    def validate_receiver_id(self, key, value):
        if self.name == BookActionName.RELEASE:
            self.validate_number(value)
        else:
            assert value is None
        return value

    @validates('comment')
    def validate_comment(self, key, value):
        if value is not None:
            length = len(value.encode('utf-8'))
            assert isinstance(value, str) and length < 256, \
                'The comment must be less than 256 utf-8 characters long'
        return value

    def validate_number(self, value):
        assert value and isinstance(value, int) and value > 0, \
            'Number must be integer greater than zero'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save_in_transaction(self):
        db.session.add(self)

    def delete_in_transaction(self):
        db.session.delete(self)

    def format_for_catalog(self, get_receiver):
        displayed_names = {
            1: 'otrzymano',
            2: 'wydano',
            3: 'sprzedano'
        }
        receiver = ''
        if self.receiver_id:
            receiver = get_receiver(self.receiver_id)['name']

        return {
            'id': self.id,
            'name': displayed_names[self.name.value],
            'copies': self.copies,
            'receiver': receiver,
            'comment': self.comment or '',
            'inserted_at': self.inserted_at.strftime('%d-%m-%Y')
        }

    def __repr__(self):
        return f'''
<BookAction
    id: {self.id},
    name: {self.name},
    copies: {self.copies},
    book_id: {self.book_id},
    receiver_id: {self.receiver_id},
    comment: {self.comment},
    inserted_at: {self.inserted_at}
>'''
