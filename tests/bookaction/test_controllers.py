from tests.fixture import client
from app.bookaction.models import BookAction, BookActionName
from app.catalog.models import Book
from app.receiver.models import Receiver
from app import db


def test_it_creates_receive_book_action(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 5})
    action = BookAction.query.get(1)
    assert response.status_code == 201
    assert response.get_json()['status'] == 201
    assert action.name == BookActionName.RECEIVE
    assert action.copies == 5


def test_it_returns_404_if_received_book_does_not_exist(client):
    response = client.post('/receive/1', json={'copies': 5})
    assert response.status_code == 404
    assert response.get_json()['status'] == 404
    assert 'error' in response.get_json()
    assert not BookAction.query.get(1)


def test_it_returns_400_if_received_book_with_invalid_data(client):
    create_book()
    response = client.post('/receive/1', json={'copies': 0})
    data = response.get_json()
    assert response.status_code == 400
    assert data['status'] == 400
    assert 'error' in data
    assert not BookAction.query.get(1)


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


def create_book():
    book = Book('Test book')
    book.save()


def create_receiver():
    receiver = Receiver('Paweł', 'Niesiołowski')
    receiver.save()
