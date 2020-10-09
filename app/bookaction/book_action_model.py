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
        assert value and isinstance(value, int) and value > 0,\
            {'copies': 'Liczba egzemplarzy musi być większa od zera'}
        return value

    @validates('book_id')
    def validate_book_id(self, key, value):
        assert value and isinstance(value, int) and value > 0
        return value

    @validates('receiver_id')
    def validate_receiver_id(self, key, value):
        if self.name == BookActionName.RELEASE:
            assert value and isinstance(value, int) and value > 0
        else:
            assert value is None or (isinstance(value, int) and value > 0)
        return value

    @validates('comment')
    def validate_comment(self, key, value):
        if value is not None:
            length = len(value.encode('utf-8'))
            assert isinstance(value, str) and length < 256,\
                {'comment': 'Komentarz musi mieć mniej niż 256 znaków'}
        return value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

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
