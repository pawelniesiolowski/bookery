from app.receiver.receiver_model import Receiver
import pytest


def test_it_is_created_with_name_and_surname():
    assert Receiver('Paweł', 'Niesiołowski')


def test_it_raises_error_with_name_equals_empty_string():
    with pytest.raises(AssertionError):
        Receiver('', 'Niesiołowski')


def test_it_raises_error_with_surname_equals_empty_string():
    with pytest.raises(AssertionError):
        Receiver('Paweł', '')


def test_it_raises_error_with_empty_name():
    with pytest.raises(AssertionError):
        Receiver(None, 'Niesiołowski')


def test_it_raises_error_with_empty_surname():
    with pytest.raises(AssertionError):
        Receiver('Paweł', None)


def test_it_raises_error_when_name_is_to_long():
    with pytest.raises(AssertionError):
        Receiver('Abcdefghijabcdefghijabcdef', 'Niesiołowski')


def test_it_raises_error_when_name_is_to_short():
    with pytest.raises(AssertionError):
        Receiver('A', 'Niesiołowski')


def test_it_raises_error_when_surname_is_to_long():
    surname = 'Abcdefghijabcdefghijabcd-Abcdefghijabcdefghijabcde Abcde'
    with pytest.raises(AssertionError):
        Receiver('Paweł', surname)


def test_it_raises_error_when_surname_is_to_short():
    with pytest.raises(AssertionError):
        Receiver('Paweł', 'N')


def test_it_can_be_deleted():
    receiver = Receiver('Paweł', 'Niesiołowski')
    receiver.delete()
    assert receiver.deleted_at
