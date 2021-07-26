"""Repository"""


from typing import List, Optional
from .models import Book


def books_ordered_by_title() -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        Book.title.asc()
        ).all()


def books_ordered_by_date() -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        Book.inserted_at.desc()
        ).all()


def books_ordered_by_authors() -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        Book.authors.asc()
        ).all()


def books_ordered_by_publication_year() -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        Book.publication_year.asc()
        ).all()


def book_by_id(book_id: int) -> Optional[Book]:
    return Book.query.get(book_id)


def does_title_exist(title: str) -> bool:
    return Book.query.filter(Book.title == title).count() > 0
