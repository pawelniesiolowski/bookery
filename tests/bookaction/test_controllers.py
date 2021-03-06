"""Test controllers"""
# pylint: disable=redefined-outer-name


import pytest
# pylint: disable=unused-import
from tests.fixture import client
# pylint: enable=unused-import
from app.bookaction.models import BookAction, BookActionName
from app.catalog.models import Book
from app.receiver.models import Receiver


@pytest.mark.webtest
def test_it_creates_receive_book_action(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 5})
    action = BookAction.query.get(1)
    assert response.status_code == 201
    assert response.get_json()['status'] == 201
    assert action.name == BookActionName.RECEIVE
    assert action.copies == 5


@pytest.mark.webtest
def test_it_returns_404_if_received_book_does_not_exist(client):
    response = client.post('/receive/1', json={'copies': 5})
    assert response.status_code == 404
    assert response.get_json()['status'] == 404
    assert 'error' in response.get_json()
    assert not BookAction.query.get(1)


@pytest.mark.webtest
def test_it_returns_400_if_received_book_with_invalid_data(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 0})
    data = response.get_json()
    assert response.status_code == 400
    assert data['status'] == 400
    assert 'error' in data
    assert not BookAction.query.get(1)


@pytest.mark.webtest
def test_it_creates_release_book_action(client):
    create_book()
    create_receiver()
    client.post('/receive/1', json={'copies': 5})
    response = client.post('/release/1', json={
        'copies': 3,
        'receiver': 1,
        'comment': 'Testowy komentarz'
    })
    action = BookAction.query.get(2)
    assert response.status_code == 201
    assert response.get_json()['status'] == 201
    assert action.name == BookActionName.RELEASE
    assert action.copies == 3


@pytest.mark.webtest
def test_it_creates_sell_book_action(client):
    create_book()
    create_receiver()
    client.post('/receive/1', json={'copies': 10})
    response = client.post('/sell/1', json={'copies': 5})
    action = BookAction.query.get(2)
    assert response.status_code == 201
    assert response.get_json()['status'] == 201
    assert action.name == BookActionName.SELL
    assert action.copies == 5


@pytest.mark.webtest
def test_it_returns_404_if_gets_invalid_receiver_id(client):
    create_book()
    client.post('/receive/1', json={'copies': 5})
    response = client.post('/release/1', json={
        'copies': 3,
        'receiver': '',
        'comment': 'Testowy komentarz'
    })
    assert response.status_code == 404
    assert response.get_json()['status'] == 404
    assert 'error' in response.get_json()
    assert not BookAction.query.get(2)


@pytest.mark.webtest
def test_it_returns_400_if_gets_invalid_copies_data(client):
    create_book()
    create_receiver()
    client.post('/receive/1', json={'copies': 5})
    response = client.post('/release/1', json={
        'copies': '',
        'receiver': 1,
        'comment': 'Testowy komentarz'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['status'] == 400
    assert 'error' in data
    assert not BookAction.query.get(2)


def create_book():
    book = Book('Test book')
    book.save()


def create_receiver():
    receiver = Receiver('Paweł', 'Niesiołowski')
    receiver.save()


# pylint: enable=redefined-outer-name
