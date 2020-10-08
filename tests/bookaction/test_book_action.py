from app.bookaction.book_action_model import BookAction, BookActionName
import pytest


def test_default_values():
    assert BookAction(BookActionName.RECEIVE, 5, book_id=1)


def test_it_throws_exception_with_release_action_without_receiver_id():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RELEASE, 5, book_id=1)


def test_it_is_created_with_release_action_and_receiver_id():
    BookAction(BookActionName.RELEASE, 5, book_id=1, receiver_id=1)


def test_it_throws_exceptions_with_zero_copies():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RECEIVE, 0, book_id=1)


def test_it_throws_exceptions_with_less_than_zero_copies():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RECEIVE, -1, book_id=1)


def test_it_contains_comment():
    book_action = BookAction(BookActionName.RECEIVE, 1, book_id=1)
    book_action.comment = 'Test comment'
    assert book_action.comment == 'Test comment'


def test_comment_could_be_none():
    assert BookAction(BookActionName.RECEIVE, 1, book_id=1, comment=None)
