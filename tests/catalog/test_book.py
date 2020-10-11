from app.catalog.models import Book
import pytest
from decimal import Decimal


def test_it_is_created_with_title():
    assert Book('Test title')


def test_it_has_inserted_at_value():
    assert Book('Test title').inserted_at


def test_it_raises_error_with_empty_title():
    with pytest.raises(AssertionError):
        Book(None)


def test_it_raises_error_with_title_as_empty_string():
    with pytest.raises(AssertionError):
        Book('')


def test_it_is_created_with_empty_authors():
    assert Book('Test title', authors=None)


def test_it_raises_error_with_authors_as_empty_string():
    with pytest.raises(AssertionError):
        Book('Test title', authors='')


def test_it_is_created_with_valid_isbn():
    assert Book('Test title', isbn='83-89533-13-8')


def test_it_raises_error_with_invalid_isbn():
    with pytest.raises(AssertionError):
        Book('Test title', isbn='83-89533-13-8-1')


def test_it_raises_error_with_price_equals_less_than_zero():
    with pytest.raises(AssertionError):
        Book('Test title', price=-1)


def test_it_rounds_price_up():
    assert Decimal('10.99') == Book('Test title', price=10.985).price


def test_it_raises_error_if_price_is_to_high():
    with pytest.raises(AssertionError):
        Book('Test title', price=100000)


def test_optional_values_can_be_none():
    assert Book('Test title', authors=None, isbn=None, price=None)


def test_it_can_be_deleted():
    book = Book('Test Book')
    book.delete()
    assert book.deleted_at
