from tests.fixture import client
from app.receiver.receiver_model import Receiver


def test_it_gets_new_receiver_form(client):
    response = client.get('/receivers/form')
    expected_text = '<h2 class="bookery-subtitle">Dodaj użytkownika</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_creates_receiver(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    expected_text = 'Dodano użytkownika: Paweł Niesiołowski'
    response = client.post(
        '/receivers/form',
        data=receiver,
        follow_redirects=True
    )
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_shows_error_if_receiver_has_empty_name(client):
    response = client.post(
        '/receivers/form',
        data={'name': '', 'surname': 'Niesiołowski'}
    )
    assert response.status_code == 200
    assert 'Imię jest wymagane' in response.get_data(as_text=True)


def test_it_shows_error_if_receiver_has_empty_surname(client):
    response = client.post(
        '/receivers/form',
        data={'name': 'Paweł', 'surname': ''}
    )
    assert response.status_code == 200
    assert 'Nazwisko jest wymagane' in response.get_data(as_text=True)


def test_it_gets_edit_receiver_form(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    response = client.get('/receivers/1/form')
    expected_text = '<h2 class="bookery-subtitle">\
Edytuj dane użytkownika: Paweł Niesiołowski</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_edits_receiver(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    edited_receiver = {'name': 'Marek', 'surname': 'Niesiołowski'}
    response = client.post(
        '/receivers/1/form',
        data=edited_receiver,
        follow_redirects=True
    )
    expected_text = 'Zmieniono dane użytkownika: Marek Niesiołowski'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


def test_it_deletes_receiver(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    response = client.delete('/receivers/1')
    assert response.status_code == 204
    assert Receiver.query.get(1).deleted_at
