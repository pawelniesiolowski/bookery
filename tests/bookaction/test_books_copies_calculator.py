import pytest
from app.bookaction.models import BookAction, BookActionName
from app.bookaction.books_copies_calculator import calculate


def test_it_calculates_copies_for_books_ids():
    books_ids = [1, 2, 3, 4]

    events = [
        BookAction(BookActionName.RECEIVE, 5, book_id=1),
        BookAction(BookActionName.RECEIVE, 10, book_id=2),
        BookAction(BookActionName.RECEIVE, 15, book_id=3),
        BookAction(BookActionName.RELEASE, 3, book_id=2, receiver_id=1),
        BookAction(BookActionName.RELEASE, 2, book_id=1, receiver_id=1),
        BookAction(BookActionName.RECEIVE, 1, book_id=4),
        BookAction(BookActionName.SELL, 4, book_id=3),
        BookAction(BookActionName.RECEIVE, 3, book_id=1),
    ]

    expected = {
        1: 6,
        2: 7,
        3: 11,
        4: 1
    }

    assert calculate(books_ids, events) == expected


def test_it_calculates_zero_copies_for_books_ids_without_events():
    books_ids = [1]

    events = []

    expected = {1: 0}

    assert calculate(books_ids, events) == expected
