from tests.fixture import client
from app.catalog.models import Book
from app import db


def test_it_gets_new_receiver_form(client):
    response = client.get('/books/form')
    expected_text = '<h2 class="bookery-subtitle">Dodaj książkę</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_creates_book(client):
    book = {'title': 'Test Book'}
    expected_text = 'Dodano książkę: Test Book'
    response = client.post('/books/form', data=book, follow_redirects=True)
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_shows_error_if_book_has_empty_title(client):
    response = client.post('/books/form', data={'title': ''})
    assert response.status_code == 200
    assert 'Tytuł jest wymagany' in response.get_data(as_text=True)


def test_it_shows_one_book(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    expected_text = '<h2 class="bookery-subtitle">"Test Book"</h2>'
    response = client.get('/books/1')
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_gets_edit_receiver_form(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    response = client.get('/books/1/form')
    expected_text = '<h2 class="bookery-subtitle">\
Edytuj książkę: Test Book</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_edits_book(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    edited_book = {'title': 'Edited Test Book'}
    response = client.post(
        '/books/1/form',
        data=edited_book,
        follow_redirects=True
    )
    expected_text = 'Zmieniono dane książki: Edited Test Book'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_deletes_book(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    response = client.delete('/books/1')
    assert response.status_code == 204
    assert Book.query.get(1).deleted_at


def test_it_returns_true_if_book_with_given_title_exists(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    response = client.get('/books/Test Book/exists')
    assert response.status_code == 200
    assert response.get_json()['data'] is True


def test_it_returns_true_if_book_with_given_title_exists(client):
    book = {'title': 'Test Book'}
    client.post('/books/form', data=book)
    response = client.get('/books/Test Book 2/exists')
    assert response.status_code == 200
    assert response.get_json()['data'] is False
