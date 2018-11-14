import json
import pytest

from run import app
from tests.v2.sample_data import USERS, HEADERS


# @pytest.fixture
# def auth_client():
#     """
#     Returns app to be used in testing api routes
#     """
#     client = app.test_client()
#     ctx = app.app_context()
#     ctx.push()
#     yield client
#     ctx.pop()


def test_registration(auth_client):
    """Test fresh registration of user."""
    response = auth_client.post('/auth/register', data=json.dumps(USERS['user3']), headers=HEADERS)

    assert response.status_code == 201


def test_user_login(auth_client):
    """ Test whether registered user can login."""
    username = USERS['user3']['username']
    password = USERS['user3']['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = auth_client.post('auth/login', data=json.dumps(credentials), headers=HEADERS)

    assert response.status_code == 200


def test_already_registered_user(auth_client):
    """ Test registered user who wants to register again"""
    response = auth_client.post('/auth/register', data=json.dumps(USERS['user3']), headers=HEADERS)

    assert response.status_code == 400


def test_unregistered_user_login(auth_client):
    """ Test unregistered users who want to login"""
    expected_message = 'user does not exist'
    """ Test whether registered user can login."""
    username = USERS['user4']['username']
    password = USERS['user4']['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = auth_client.post('auth/login', data=json.dumps(credentials), headers=HEADERS)
    data = response.json
    assert response.status_code == 404
    assert data['message'] == expected_message
