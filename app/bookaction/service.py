"""Interface for accessing Book Actions's data from external modules"""


from typing import List, Dict, Tuple
from datetime import datetime
from app.receiver import service as receiver
from . import repo
from .book import Book
from . import books_copies_calculator


def copies_for_book(book_id: int) -> int:
    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    return book.copies.to_int()


def maybe_copies_for_book_before_date(
        book_id: int,
        before_date: datetime
        ) -> Tuple[int, int]:
    actions = repo.actions_before_date_ordered_by_date_asc(
            book_id,
            before_date
            )
    book = Book(actions, book_id=book_id)
    return (len(actions), book.copies.to_int())


def copies_for_books(books_ids: List[int]) -> Dict[int, int]:
    actions = repo.all_actions_ordered_by_date_desc()
    return books_copies_calculator.calculate(books_ids, actions)


def actions_for_book(book_id: int) -> List[Dict]:
    actions = repo.actions_ordered_by_date_desc(book_id)
    return [
        action.format_for_catalog(receiver.get_receiver)
        for action in actions
        ]
