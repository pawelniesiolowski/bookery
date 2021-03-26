"""Repository"""


from typing import List, Optional
from .models import Book


def books_ordered_by_title() -> List[Book]:
    return Book.query.filter(
        Book.deleted_at.is_(None)
        ).order_by(
        Book.title.asc()
        ).all()


def book_by_id(book_id: int) -> Optional[Book]:
    return Book.query.get(book_id)


def does_title_exist(title: str) -> bool:
    return Book.query.filter(Book.title == title).count() > 0
