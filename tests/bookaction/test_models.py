from app.bookaction.models import BookAction, BookActionName
import pytest


def test_it_is_created_with_receive_action():
    assert BookAction(BookActionName.RECEIVE, 5, book_id=1)


def test_it_is_created_with_release_action_and_receiver_id():
    BookAction(BookActionName.RELEASE, 5, book_id=1, receiver_id=1)


def test_it_raises_error_with_release_action_without_receiver_id():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RELEASE, 5, book_id=1)


def test_it_raises_error_with_receive_action_and_receiver_id():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RECEIVE, 5, book_id=1, receiver_id=1)


def test_it_raises_error_with_zero_copies():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RECEIVE, 0, book_id=1)


def test_it_raises_error_with_less_than_zero_copies():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.RECEIVE, -1, book_id=1)


def test_it_contains_comment():
    book_action = BookAction(BookActionName.RECEIVE, 1, book_id=1)
    book_action.comment = 'Test comment'
    assert book_action.comment == 'Test comment'


def test_comment_could_be_none():
    assert BookAction(BookActionName.RECEIVE, 1, book_id=1, comment=None)


def test_it_is_created_with_sell_action():
    BookAction(BookActionName.SELL, 5, book_id=1)


def test_it_raises_error_with_sell_action_and_receiver_id():
    with pytest.raises(AssertionError):
        BookAction(BookActionName.SELL, 5, book_id=1, receiver_id=1)


def test_it_creates_receive_action_name_for_catalog():
    action = BookAction(BookActionName.RECEIVE, 5, book_id=1)
    catalog_action = action.format_for_catalog(None)
    assert catalog_action['name'] == 'otrzymano'


def test_it_creates_release_action_name_for_catalog():
    action = BookAction(BookActionName.RELEASE, 5, book_id=1, receiver_id=1)
    catalog_action = action.format_for_catalog(lambda id: {'name': 'Anonim'})
    assert catalog_action['name'] == 'wydano'


def test_it_creates_sell_action_name_for_catalog():
    action = BookAction(BookActionName.SELL, 5, book_id=1)
    catalog_action = action.format_for_catalog(lambda id: {'name': 'Anonim'})
    assert catalog_action['name'] == 'sprzedano'


def test_it_creates_empty_string_for_empty_comment():
    action = BookAction(BookActionName.RELEASE, 5, book_id=1, receiver_id=1)
    catalog_action = action.format_for_catalog(lambda id: {'name': 'Anonim'})
    assert catalog_action['comment'] == ''
