from .models import BookAction
from . import repo
from .book import Book
from app.receiver import service as receiver_service
from . import books_copies_calculator


def copies_for_book(book_id):
    book = Book(repo.actions_ordered_by_date_asc(book_id), book_id=book_id)
    return book.copies.to_int()


def copies_for_books(books_ids):
    actions = repo.all_actions_ordered_by_date_desc()
    return books_copies_calculator.calculate(books_ids, actions)


def actions_for_book(book_id):
    actions = repo.actions_ordered_by_date_desc(book_id)
    return [
        action.format_for_catalog(receiver_service.get_receiver)
        for action in actions
    ]
