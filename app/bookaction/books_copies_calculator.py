from .book import Book
from .models import BookAction


def calculate(books_ids, events):
    assert isinstance(books_ids, list) and isinstance(events, list)

    events_for_ids = {}
    for book_id in books_ids:
        if not isinstance(book_id, int):
            raise ValueError('Book id must be integer number')
        events_for_ids[book_id] = []

    for event in events:
        if not isinstance(event, BookAction):
            raise ValueError('Event must be BookAction class')
        if event.book_id in events_for_ids:
            events_for_ids[event.book_id].append(event)

    copies_for_ids = {}
    for checked_id in events_for_ids:
        book = Book(events_for_ids[checked_id], book_id=checked_id)
        copies_for_ids[checked_id] = book.copies.to_int()

    return copies_for_ids
