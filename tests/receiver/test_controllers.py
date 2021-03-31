"""Test controllers"""
# pylint: disable=redefined-outer-name

import pytest
# pylint: disable=unused-import
from tests.fixture import client
# pylint: enable=unused-import
from app.receiver.models import Receiver


@pytest.mark.webtest
def test_it_gets_new_receiver_form(client):
    response = client.get('/receivers/form')
    expected_text = '<h2 class="bookery-subtitle">Dodaj użytkownika</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


@pytest.mark.webtest
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


@pytest.mark.webtest
def test_it_shows_error_if_receiver_has_empty_name(client):
    response = client.post(
        '/receivers/form',
        data={'name': '', 'surname': 'Niesiołowski'}
    )
    assert response.status_code == 200
    assert 'Imię jest wymagane' in response.get_data(as_text=True)


@pytest.mark.webtest
def test_it_shows_error_if_receiver_has_empty_surname(client):
    response = client.post(
        '/receivers/form',
        data={'name': 'Paweł', 'surname': ''}
    )
    assert response.status_code == 200
    assert 'Nazwisko jest wymagane' in response.get_data(as_text=True)


@pytest.mark.webtest
def test_it_gets_edit_receiver_form(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    response = client.get('/receivers/1/form')
    expected_text = '<h2 class="bookery-subtitle">\
Edytuj dane użytkownika: Paweł Niesiołowski</h2>'
    assert response.status_code == 200
    assert expected_text in response.get_data(as_text=True)


@pytest.mark.webtest
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


@pytest.mark.webtest
def test_it_deletes_receiver(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    response = client.delete('/receivers/1')
    assert response.status_code == 204
    assert Receiver.query.get(1).deleted_at


@pytest.mark.webtest
def test_it_does_not_create_receiver_that_already_exists(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    response = client.post('/receivers/form', data=receiver)
    expected_text = 'Użytkownik: Paweł Niesiołowski już istnieje'
    assert expected_text in response.get_data(as_text=True)


@pytest.mark.webtest
def test_it_undeletes_deleted_receiver_if_it_is_created(client):
    receiver = {'name': 'Paweł', 'surname': 'Niesiołowski'}
    client.post('/receivers/form', data=receiver)
    client.delete('/receivers/1')
    assert Receiver.query.get(1).deleted_at is not None
    client.post('/receivers/form', data=receiver)
    assert Receiver.query.get(1).deleted_at is None


@pytest.mark.webtest
def test_it_gets_receivers_data(client):
    client.post('/receivers/form', data={
        'name': 'Paweł',
        'surname': 'Niesiołowski'
    })
    client.post('/receivers/form', data={
        'name': 'Justyna',
        'surname': 'Mazur'
    })
    response = client.get('/receivers')
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == 200
    assert len(data['data']) == 2


# pylint: enable=redefined-outer-name
