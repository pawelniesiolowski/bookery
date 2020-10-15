from .models import BookAction
from .repo import actions_ordered_by_date_asc, actions_ordered_by_date_desc
from .book import Book
from app.receiver.service import get_receiver


def copies_for_book(book_id):
    book = Book(actions_ordered_by_date_asc(book_id), book_id=book_id)
    return book.copies.to_int()


def actions_for_book(book_id):
    actions = actions_ordered_by_date_desc(book_id)
    return [action.format_for_catalog(get_receiver) for action in actions]
