from .. import db
from datetime import datetime
from sqlalchemy.orm import validates
from .isbn_validator import ISBNValidator
from decimal import Decimal, ROUND_UP


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    authors = db.Column(db.String(500), nullable=True)
    isbn = db.Column(db.String(17), nullable=True)
    price = db.Column(db.Numeric(7, 2), nullable=True)
    publication_year = db.Column(db.Numeric(4, 0), nullable=True)
    inserted_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, title, **kwargs):
        super(Book, self).__init__(**kwargs)
        self.title = title
        self.inserted_at = datetime.now()

    @validates('title')
    def validate_title(self, key, value):
        assert value and isinstance(value, str)
        return value

    @validates('authors')
    def validate_authors(self, key, value):
        assert value is None or (value and isinstance(value, str))
        return value

    @validates('isbn')
    def validate_isbn(self, key, value):
        assert value is None or ISBNValidator.is_valid(value)
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not value:
            return None
        value = Decimal(value).quantize(Decimal('.01'), rounding=ROUND_UP)
        assert value and value > Decimal('0') and value < Decimal('100000')
        return value

    @validates('publication_year')
    def validate_publication_year(self, key, value):
        if not value:
            return None
        value = Decimal(value).quantize(Decimal('1.'), rounding=ROUND_UP)
        assert value and value > Decimal('0') and value <= datetime.now().year
        return value

    def to_basic_data(self):
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'price': self.price,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.deleted_at = datetime.now()

    def __repr__(self):
        return f'''
<Book
    id: {self.id},
    title: {self.title},
    authors: {self.authors},
    isbn: {self.isbn},
    price: {self.price},
    publication_year: {self.publication_year},
    inserted_at: {self.inserted_at},
    deleted_at: {self.deleted_at}
>'''
