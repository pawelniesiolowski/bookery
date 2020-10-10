from app.bookaction.book import Book
from app.bookaction.book_action_model import BookAction, BookActionName


def test_it_calculates_copies_from_events():
    actions = [
        BookAction(BookActionName.RECEIVE, 2, book_id=1),
        BookAction(BookActionName.RECEIVE, 3, book_id=1)
    ]
    book = Book(actions)
    assert book.copies == 5
