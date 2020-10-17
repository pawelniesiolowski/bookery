from app.bookaction.book import Book, Copies
from app.bookaction.models import BookAction, BookActionName
import pytest


def test_it_calculates_copies_from_receive_events():
    actions = [
        BookAction(BookActionName.RECEIVE, 2, book_id=1),
        BookAction(BookActionName.RECEIVE, 3, book_id=1)
    ]
    book = Book(actions, book_id=1)
    assert book.copies.to_int() == 5


def test_it_calculates_copies_from_receive_and_release_events():
    actions = [
        BookAction(BookActionName.RECEIVE, 3, book_id=1),
        BookAction(BookActionName.RECEIVE, 6, book_id=1),
        BookAction(BookActionName.RELEASE, 2, book_id=1, receiver_id=1),
        BookAction(BookActionName.RELEASE, 5, book_id=1, receiver_id=1)
    ]
    book = Book(actions, book_id=1)
    assert book.copies.to_int() == 2


def test_it_calculates_copies_from_receive_release_and_sell_events():
    actions = [
        BookAction(BookActionName.RECEIVE, 3, book_id=1),
        BookAction(BookActionName.RECEIVE, 6, book_id=1),
        BookAction(BookActionName.RELEASE, 2, book_id=1, receiver_id=1),
        BookAction(BookActionName.SELL, 3, book_id=1)
    ]
    book = Book(actions, book_id=1)
    assert book.copies.to_int() == 4


def test_it_receive_books():
    book = Book([], book_id=1)
    action = book.receive(Copies(4))
    assert action.name == BookActionName.RECEIVE
    assert action.copies == 4
    assert book.copies.to_int() == 4


def test_it_release_books():
    book = Book([], book_id=1)
    book.receive(Copies(4))
    action = book.release(Copies(2), receiver_id=1)
    assert action.name == BookActionName.RELEASE
    assert action.copies == 2
    assert book.copies.to_int() == 2


def test_it_sell_books():
    book = Book([], book_id=1)
    book.receive(Copies(8))
    action = book.sell(Copies(2))
    assert action.name == BookActionName.SELL
    assert action.copies == 2
    assert book.copies.to_int() == 6


def test_it_raises_error_if_calculates_less_copies_than_zero():
    with pytest.raises(AssertionError):
        book = Book([], book_id=1)
        book.receive(Copies(4))
        action = book.release(Copies(5), receiver_id=1)


def test_it_sells_released_books():
    BookAction.save_in_transaction = lambda self: setattr(self, 'saved', True)
    BookAction.delete_in_transaction = (
        lambda self: setattr(self, 'deleted', True)
    )
    released = BookAction(
        BookActionName.RELEASE,
        5,
        book_id=1,
        receiver_id=1,
        id=2
    )
    actions = [
        BookAction(BookActionName.RECEIVE, 10, book_id=1),
        released
    ]
    book = Book(actions, book_id=1)
    action = book.sell_released(Copies(3), release_id=2)
    assert action.name == BookActionName.SELL
    assert action.copies == 3
    assert released.copies == 2
    assert not hasattr(released, 'deleted')
    assert released.saved


def test_it_sells_all_released_books():
    BookAction.save_in_transaction = lambda self: setattr(self, 'saved', True)
    BookAction.delete_in_transaction = (
        lambda self: setattr(self, 'deleted', True)
    )
    released = BookAction(
        BookActionName.RELEASE,
        5,
        book_id=1,
        receiver_id=1,
        id=2
    )
    actions = [
        BookAction(BookActionName.RECEIVE, 10, book_id=1),
        released
    ]
    book = Book(actions, book_id=1)
    action = book.sell_released(Copies(5), release_id=2)
    assert action.name == BookActionName.SELL
    assert action.copies == 5
    assert released.deleted


def test_it_raises_error_if_selled_copies_are_greater_than_released_copies():
    BookAction.save_in_transaction = lambda self: None
    BookAction.delete_in_transaction = lambda self: None
    released = BookAction(
        BookActionName.RELEASE,
        5,
        book_id=1,
        receiver_id=1,
        id=2
    )
    actions = [
        BookAction(BookActionName.RECEIVE, 10, book_id=1),
        released
    ]
    book = Book(actions, book_id=1)
    with pytest.raises(ValueError):
        book.sell_released(Copies(6), release_id=2)


def test_it_raises_error_if_released_id_does_not_exist():
    BookAction.save_in_transaction = lambda self: None
    BookAction.delete_in_transaction = lambda self: None
    released = BookAction(
        BookActionName.RELEASE,
        5,
        book_id=1,
        receiver_id=1,
        id=2
    )
    actions = [
        BookAction(BookActionName.RECEIVE, 10, book_id=1),
        released
    ]
    book = Book(actions, book_id=1)
    with pytest.raises(ValueError):
        book.sell_released(Copies(3), release_id=3)


def test_it_raises_error_if_selled_copies_equals_to_zero():
    BookAction.save_in_transaction = lambda self: None
    BookAction.delete_in_transaction = lambda self: None
    released = BookAction(
        BookActionName.RELEASE,
        5,
        book_id=1,
        receiver_id=1,
        id=2
    )
    actions = [
        BookAction(BookActionName.RECEIVE, 10, book_id=1),
        released
    ]
    book = Book(actions, book_id=1)
    with pytest.raises(AssertionError):
        book.sell_released(Copies(0), release_id=3)
