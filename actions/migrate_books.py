from flask_script import Command
import csv
import json
from decimal import Decimal
from datetime import datetime
from app.catalog.models import Book
from app.catalog.isbn_validator import ISBNValidator


class BooksMigrator(Command):
    def run(self):
        with open('data/book.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row['title']
                authors = self.prepare_authors(row['authors'])
                isbn = self.prepare_isbn(row['isbn'])
                price = self.prepare_price(row['price'])
                deleted_at = self.prepare_deleted_at(row['deleted_at'])
                if deleted_at is not None:
                    print(f'Omit book: {title}')
                    continue
                try:
                    book = Book(
                        title,
                        authors=authors,
                        isbn=isbn,
                        price=price,
                        deleted_at=deleted_at
                    )
                except AssertionError:
                    book = Book(
                        title,
                        authors=authors,
                        isbn=None,
                        price=price,
                        deleted_at=deleted_at
                    )
                book.save()
                print(f'Inserted book: {book}')


    def prepare_authors(self, authors):
        authors = json.loads(authors)
        if authors:
            return authors[0]['surname'] + ' ' + authors[0]['name']
        else:
            return None

    def prepare_isbn(self, isbn):
        if isbn == 'NULL':
            return None
        else:
            return isbn

    def prepare_price(self, price):
        price = Decimal(price)
        if price > 0:
            return price
        else:
            return None

    def prepare_deleted_at(self, deleted_at):
        if deleted_at == 'NULL':
            return None
        else:
            return datetime.fromisoformat(deleted_at)
