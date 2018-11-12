import json
import pytest
from storemanager import create_app
from tests.v2.sample_data import *
from flask_jwt_extended import JWTManager


@pytest.fixture
def client():
    """
    Returns app to be used in testing api routes
    """
    testing_app = create_app("testing")
    client = testing_app.test_client()
    jwt = JWTManager(testing_app)
    ctx = testing_app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture
def authorize_admin(client):
    """
    Registers and signs in user with role admin.
    Returns header to be used in testing admin
    """
    client.post('/auth/register', data=json.dumps(USERS['user2']), headers=HEADERS)

    user = USERS['user2']
    username = user['username']
    password = user['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = client.post('/auth/login', data=json.dumps(credentials), headers=HEADERS)
    data = response.json
    token = data['access_token']
    header_admin = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    assert response.status_code == 200
    return header_admin


@pytest.fixture
def authorize_attendant(client, authorize_admin):
    headers = authorize_admin
    """
        Registers and signs in user with role attendant.
        Returns header to be used in testing attendant
        """
    client.post('/api/v2/users', data=json.dumps(USERS['user1']), headers=headers)

    user = USERS['user1']
    username = user['username']
    password = user['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = client.post('/auth/login', data=json.dumps(credentials), headers=HEADERS)
    data = response.json
    token = data['access_token']
    header_attendant = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    assert response.status_code == 200
    return header_attendant
