from .models import BookAction
from .repo import actions_ordered_by_date
from .book import Book


def copies_for_book(book_id):
    book = Book(actions_ordered_by_date(book_id), book_id=book_id)
    return book.copies.to_int()
