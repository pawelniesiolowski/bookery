"""Database models"""


from datetime import datetime
from decimal import Decimal, ROUND_UP
from typing import Dict, Optional, Union
from sqlalchemy.orm import validates
from flask_sqlalchemy.model import DefaultMeta
from .. import db
from . import isbn_validator


BaseModel: DefaultMeta = db.Model


class Book(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    authors = db.Column(db.String(500), nullable=True)
    isbn = db.Column(db.String(17), nullable=True)
    price = db.Column(db.Numeric(7, 2), nullable=True)
    publication_year = db.Column(db.Numeric(4, 0), nullable=True)
    image_name = db.Column(db.String(255), nullable=True)
    inserted_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, title: str, **kwargs: Union[str, Decimal, int]) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.inserted_at = datetime.now()

    # pylint: disable=unused-argument,no-self-use

    @validates('title')
    def validate_title(self, key: str, value: str) -> str:
        assert value and isinstance(value, str)
        return value

    @validates('authors')
    def validate_authors(
            self,
            key: str,
            value: Optional[str]
            ) -> Optional[str]:
        assert value is None or (value and isinstance(value, str))
        return value

    @validates('isbn')
    def validate_isbn(
            self,
            key: str,
            value: Optional[str]
            ) -> Optional[str]:
        assert value is None or isbn_validator.is_valid(value)
        return value

    @validates('price')
    def validate_price(
            self,
            key: str,
            value: Optional[Decimal]
            ) -> Optional[Decimal]:
        if not value:
            return None
        value = Decimal(value).quantize(Decimal('.01'), rounding=ROUND_UP)
        assert value and (Decimal('0') < value < Decimal('100000'))
        return value

    @validates('publication_year')
    def validate_publication_year(
            self,
            key: str,
            value: Optional[Decimal]
            ) -> Optional[Decimal]:
        if not value:
            return None
        value = Decimal(value).quantize(Decimal('1.'), rounding=ROUND_UP)
        assert value and Decimal('0') < value <= datetime.now().year
        return value

    # pylint: enable=unused-argument,no-self-use

    def to_basic_data(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'price': self.price,
            }

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        self.deleted_at = datetime.now()

    def __repr__(self) -> str:
        return f'''
<Book
    id: {self.id},
    title: {self.title},
    authors: {self.authors},
    isbn: {self.isbn},
    price: {self.price},
    publication_year: {self.publication_year},
    image_name: {self.image_name},
    inserted_at: {self.inserted_at},
    deleted_at: {self.deleted_at}
>'''
