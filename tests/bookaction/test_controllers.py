from tests.fixture import client
from app.bookaction.book_action_model import BookAction, BookActionName
from app.catalog.book_model import Book
from app import db


def test_it_creates_receive_book_action(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 5})
    action = BookAction.query.get(1)
    assert response.status_code == 201
    assert action.name == BookActionName.RECEIVE
    assert action.copies == 5


def test_it_returns_404_if_received_book_does_not_exist(client):
    response = client.post('/receive/1', json={'copies': 5})
    assert response.status_code == 404
    assert 'error' in response.get_json()
    assert not BookAction.query.get(1)


def test_it_returns_404_if_received_book_with_invalid_data(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 0})
    assert response.status_code == 404
    assert 'copies' in response.get_json()['error']
    assert not BookAction.query.get(1)


def create_book():
    book = Book('Test book')
    book.save()
