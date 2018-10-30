"""
Module containing tests for the various endpoints.
Contains tests for both Admin User and Attendant.
"""
import json
import pytest
from run import app
from tests.v2.sample_data import PRODUCTS, SALE_RECORDS, USERS, HEADERS


@pytest.fixture
def client():
    """
    Returns app to be used in testing api routes
    """
    client = app.test_client()
    ctx = app.app_context()
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
def authorize_attendant(client):
    """
        Registers and signs in user with role attendant.
        Returns header to be used in testing attendant
        """
    client.post('/auth/register', data=json.dumps(USERS['user1']), headers=HEADERS)

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


def test_admin_add_product(client, authorize_admin):
    """admin should be able to add product"""
    headers = authorize_admin
    expected_result = {
        'id': 1,
        'name': 'Table',
        'price': 10000,
        'description': 'a cool table',
        'category': 'furniture',
        'stock': 100,
        'min_stock': 10
    }

    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product1']), headers=headers)
    data = response.json
    assert response.status_code == 201
    assert data['product'] == expected_result


def test_admin_get_all_products(client, authorize_admin):
    """admin should be able to get all products"""
    headers = authorize_admin
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product2']), headers=headers)
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product3']), headers=headers)
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product4']), headers=headers)

    response = client.get('/api/v2/products', headers=headers)
    data = response.json
    products = data['products']

    assert response.status_code == 200
    assert len(products) == 4


def test_admin_get_one_product(client, authorize_admin):
    """admin should be able to get a single product"""
    headers = authorize_admin
    expected_result = {
        'id': 3,
        'name': 'Television',
        'price': 30000,
        'description': 'a cool television',
        'category': 'electronic',
        'stock': 200,
        'min_stock': 20
    }

    response = client.get('/api/v2/products/{:d}'.format(3), headers=headers)
    data = response.json

    assert data['product'] == expected_result
    assert response.status_code == 200


def test_admin_remove_product(client, authorize_admin):
    """admin should be able to delete a product"""
    headers = authorize_admin
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product5']), headers=headers)

    response = client.delete('/api/v2/products/{:d}'.format(5), headers=headers)

    assert response.status_code == 200


def test_admin_add_sale(client, authorize_admin):
    """admin should not be able to create a sale record"""
    headers = authorize_admin
    expected_message = 'only attendants can create a sale record'

    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale1']), headers=headers)
    data = response.json

    assert response.status_code == 403
    assert data['message'] == expected_message


def test_admin_get_sales_empty(client, authorize_admin):
    """admin should be able to get all sales, this tests for empty response"""
    headers = authorize_admin
    expected_message = 'no sale records created yet'

    response = client.get('/api/v2/sales', headers=headers)
    data = response.json

    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_get_one_sale_empty(client, authorize_admin):
    """admin should be able to get a single sale, this tests for empty response"""
    headers = authorize_admin
    expected_message = 'sale with given id does not exist'

    response = client.get('/api/v2/sales/{:d}'.format(2), headers=headers)
    data = response.json

    assert response.status_code == 404
    assert data['message'] == expected_message


def test_attendant_add_product(client, authorize_attendant):
    """attendant should not be able to add new product"""
    headers = authorize_attendant
    expected_message = 'only admin can add a product'

    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product1']), headers=headers)
    data = response.json

    assert response.status_code == 403
    assert data['message'] == expected_message


def test_attendant_get_all_products(client, authorize_attendant):
    """attendant should be able to get all products"""
    headers = authorize_attendant

    response = client.get('/api/v2/products', headers=headers)
    data = response.json
    products = data['products']

    assert response.status_code == 200
    assert len(products) == 4


def test_attendant_get_one_product(client, authorize_attendant):
    """attendant should be able to get a single product"""
    headers = authorize_attendant
    expected_result = {
        'id': 3,
        'name': 'Television',
        'description': 'a cool television',
        'price': 30000,
        'category': 'electronic',
        'stock': 200,
        'min_stock': 20
    }

    response = client.get('/api/v2/products/{:d}'.format(3), headers=headers)
    data = response.json

    assert data['product'] == expected_result
    assert response.status_code == 200


def test_attendant_remove_product(client, authorize_attendant):
    """attendant should not be able to remove a product"""
    headers = authorize_attendant
    expected_message = 'only administrator can delete a product'

    response = client.delete('/api/v2/products/{:d}'.format(3), headers=headers)
    data = response.json

    assert response.status_code == 403
    assert data['message'] == expected_message


def test_attendant_add_sale(client, authorize_attendant):
    """attendant should be able to create a new sale record"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale1']), headers=headers)
    data = response.json

    assert response.status_code == 201
    assert data['sale']['items'] == 12
    assert data['sale']['total'] == 320000


def test_attendant_get_all_sales(client, authorize_attendant):
    """attendant should be able to get sale records"""
    headers = authorize_attendant
    client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale2']), headers=headers)

    response = client.get('/api/v2/sales', headers=headers)
    data = response.json

    assert response.status_code == 200
    assert len(data['sales']) == 2


def test_attendant_get_single_sale(client, authorize_attendant):
    """attendant should be able to get a single sale record"""
    headers = authorize_attendant
    expected_result = {
        "id": 2,
        "products": {
            "1": {
                "name": "Table",
                "price": 10000,
                "quantity": 2,
                "cost": 20000
            },
            "2": {
                "name": "Phone",
                "price": 20000,
                "quantity": 2,
                "cost": 40000
            },
            "3": {
                "name": "Couch",
                "price": 50000,
                "quantity": 10,
                "cost": 500000
            }
        },
        "items": 14,
        "total": 560000
    }

    response = client.get('/api/v2/sales/{:d}'.format(2), headers=headers)

    data = response.json

    assert response.status_code == 200
    assert data['sale'] == expected_result


def test_admin_get_all_sales(client, authorize_admin):
    """admin should be able to get list of sales"""
    headers = authorize_admin

    response = client.get('/api/v2/sales', headers=headers)
    data = response.json

    assert response.status_code == 200
    assert len(data['sales']) == 2


def test_admin_get_single_sale(client, authorize_admin):
    """admin should be able to get a single sale record"""
    headers = authorize_admin
    expected_result = {
        "id": 2,
        "products": {
            "1": {
                "name": "Table",
                "price": 10000,
                "quantity": 2,
                "cost": 20000
            },
            "2": {
                "name": "Phone",
                "price": 20000,
                "quantity": 2,
                "cost": 40000
            },
            "3": {
                "name": "Couch",
                "price": 50000,
                "quantity": 10,
                "cost": 500000
            }
        },
        "items": 14,
        "total": 560000
    }

    response = client.get('/api/v2/sales/{:d}'.format(2), headers=headers)

    data = response.json

    assert response.status_code == 200
    assert data['sale'] == expected_result
