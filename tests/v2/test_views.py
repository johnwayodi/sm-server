"""
Module containing tests for the various endpoints.
Contains tests for both Admin User and Attendant.
"""
import json
from tests.v2.sample_data import *


def test_admin_add_attendant(client, authorize_admin):
    """admin should be able to create an attendant account"""
    headers = authorize_admin
    expected_result = 'attendant created successfully'

    username = USERS['user4']['username']
    password = USERS['user4']['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = client.post('/api/v2/users', data=json.dumps(credentials), headers=headers)
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == expected_result


def test_admin_add_attendant_exists(client, authorize_admin):
    """admin should not be able to create same attendant account"""
    headers = authorize_admin
    expected_result = 'attendant with similar name exists'

    username = USERS['user4']['username']
    password = USERS['user4']['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = client.post('/api/v2/users', data=json.dumps(credentials), headers=headers)
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == expected_result


def test_admin_get_attendant(client, authorize_admin):
    """admin should be able to view an attendant account"""
    headers = authorize_admin
    expected_result = {
        "id": 3,
        "username": "walulu",
        "role": "attendant"
    }

    response = client.get('/api/v2/users/{:d}'.format(3), headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data['user'] == expected_result


def test_admin_get_attendant_not_exist(client, authorize_admin):
    """admin should be able to view an attendant account"""
    headers = authorize_admin
    expected_message = 'user with id does not exist'

    response = client.get('/api/v2/users/{:d}'.format(20), headers=headers)
    data = response.get_json()
    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_get_attendant_non_integer(client, authorize_admin):
    """admin should be able to pass a non integer value in url"""
    headers = authorize_admin
    expected_message = 'user id must be integer'

    response = client.get('/api/v2/users/a', headers=headers)
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_get_users(client, authorize_admin):
    """admin should be able to get all users of system"""
    headers = authorize_admin
    response = client.get('/api/v2/users', headers=headers)
    assert response.status_code == 200


def test_admin_delete_attendant_non_integer(client, authorize_admin):
    """admin should be able to pass a non integer value in url"""
    headers = authorize_admin
    expected_message = 'user id must be integer'

    response = client.delete('/api/v2/users/a', headers=headers)
    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_delete_attendant_non_existent(client, authorize_admin):
    """admin should be able to delete a non existent attendant"""
    headers = authorize_admin
    expected_message = 'user with id does not exist'

    response = client.delete('/api/v2/users/{:d}'.format(6), headers=headers)
    data = response.get_json()
    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_delete_attendant(client, authorize_admin):
    """admin should be able to delete a non existent attendant"""
    headers = authorize_admin
    expected_message = 'user deleted successfully'

    response = client.delete('/api/v2/users/{:d}'.format(3), headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == expected_message


def test_admin_add_category_empty(client, authorize_admin):
    """admin should be able to get empty category list message"""
    headers = authorize_admin
    expected_result = 'no categories added yet'

    response = client.get('/api/v2/categories', headers=headers)
    data = response.json
    assert response.status_code == 404
    assert data['message'] == expected_result


def test_admin_add_category(client, authorize_admin):
    """admin should be able to add category"""
    headers = authorize_admin
    expected_result = {
        "id": 1,
        "name": "furniture",
        "description": "this is the furniture category"
    }

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category1']), headers=headers)
    data = response.json
    assert response.status_code == 201
    assert data['category'] == expected_result


def test_admin_add_category_existing(client, authorize_admin):
    """admin should not be able to add an already existing category"""
    headers = authorize_admin
    expected_result = 'category already exists'

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category1']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_result


def test_admin_add_category_numbered(client, authorize_admin):
    """admin should not be able to add category whose name is numbers"""
    headers = authorize_admin
    expected_result = 'name cannot be an integer value'

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category5']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_result


def test_admin_add_category_empty_name(client, authorize_admin):
    """admin should not be able to add category with empty name"""
    headers = authorize_admin
    expected_result = 'please provide a category name'

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category6']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_result


def test_admin_add_category_desc_numbered(client, authorize_admin):
    """admin should not be able to add category whose description is numbers"""
    headers = authorize_admin
    expected_result = 'description cannot be an integer value'

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category7']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_result


def test_admin_get_category(client, authorize_admin):
    """admin should be able to get a category"""
    headers = authorize_admin
    expected_result = {
        "id": 1,
        "name": "furniture",
        "description": "this is the furniture category"
    }

    response = client.get('/api/v2/categories/{:d}'.format(1), headers=headers)
    data = response.json
    assert response.status_code == 200
    assert data['category'] == expected_result


def test_admin_get_categories(client, authorize_admin):
    """admin should be able to get all categories"""
    headers = authorize_admin
    response = client.post('/api/v2/categories', data=json.dumps(CATEGORIES['category2']), headers=headers)
    assert response.status_code == 201
    response = client.post('/api/v2/categories', data=json.dumps(CATEGORIES['category3']), headers=headers)
    assert response.status_code == 201
    response = client.post('/api/v2/categories', data=json.dumps(CATEGORIES['category4']), headers=headers)
    assert response.status_code == 201

    response = client.get('/api/v2/categories', headers=headers)
    data = response.json

    assert response.status_code == 200
    assert len(data['categories']) == 4


def test_admin_update_category(client, authorize_admin):
    """admin should be able to get a category"""
    headers = authorize_admin
    expected_message = 'category updated successfully'

    response = client.put('/api/v2/categories/2', data=json.dumps(UPDATED_CATEGORY),
                          headers=headers)
    data = response.json
    assert response.status_code == 200
    assert data['message'] == expected_message


def test_admin_delete_category(client, authorize_admin):
    """admin should be able to get all categories"""
    headers = authorize_admin

    response = client.delete('/api/v2/categories/{:d}'.format(3), headers=headers)
    assert response.status_code == 200


def test_admin_get_products_empty(client, authorize_admin):
    """admin should be able to get no products, as list is empty"""
    headers = authorize_admin
    expected_message = 'no products added yet'
    response = client.get('/api/v2/products', headers=headers)

    data = response.json
    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_add_product(client, authorize_admin):
    """admin should be able to add product"""
    headers = authorize_admin
    expected_result = {
        'id': 1,
        'name': 'table',
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


def test_admin_add_product_name_integer(client, authorize_admin):
    """admin should not be able to add product with name number"""
    headers = authorize_admin
    expected_message = 'name cannot be an integer value'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product6']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_name_empty(client, authorize_admin):
    """admin should not be able to add product with empty name"""
    headers = authorize_admin
    expected_message = 'name should not be empty'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product7']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_price_negative(client, authorize_admin):
    """admin should not be able to add product with negative price"""
    headers = authorize_admin
    expected_message = 'price cannot be a negative or 0'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product8']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_description_numbered(client, authorize_admin):
    """admin should not be able to add product with numbered description"""
    headers = authorize_admin
    expected_message = 'description cannot be an integer value'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product9']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_description_empty(client, authorize_admin):
    """admin should not be able to add product with empty description"""
    headers = authorize_admin
    expected_message = 'description should not be empty'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product11']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_category_numbered(client, authorize_admin):
    """admin should not be able to add product with numbered description"""
    headers = authorize_admin
    expected_message = 'category cannot be an integer value'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product10']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_category_empty(client, authorize_admin):
    """admin should not be able to add product with empty description"""
    headers = authorize_admin
    expected_message = 'category should not be empty'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product12']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_stock_negative(client, authorize_admin):
    """admin should not be able to add product with negative stock"""
    headers = authorize_admin
    expected_message = 'stock cannot be a negative or 0'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product13']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_add_product_minstock_negative(client, authorize_admin):
    """admin should not be able to add product with negative minimum stock"""
    headers = authorize_admin
    expected_message = 'minimum cannot be a negative or 0'
    response = client.post('/api/v2/products',
                           data=json.dumps(PRODUCTS['product14']), headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data['message'] == expected_message


def test_admin_get_all_products(client, authorize_admin):
    """admin should be able to get all products"""
    headers = authorize_admin
    response = client.post('/api/v2/products', data=json.dumps(PRODUCTS['product2']), headers=headers)
    assert response.status_code == 201
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product3']), headers=headers)
    assert response.status_code == 201
    response = client.post('/api/v2/products', data=json.dumps(PRODUCTS['product4']), headers=headers)
    assert response.status_code == 201
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
        'name': 'television',
        'price': 30000,
        'description': 'a cool television',
        'category': 'electronics',
        'stock': 200,
        'min_stock': 20
    }

    response = client.get('/api/v2/products/{:d}'.format(3), headers=headers)
    data = response.json

    assert response.status_code == 200
    assert data['product'] == expected_result


def test_admin_update_product(client, authorize_admin):
    """admin should be able to get a single product"""
    headers = authorize_admin
    expected_message = 'product updated successfully'

    response = client.put('/api/v2/products/{:d}'.format(3), data=json.dumps(PRODUCTS['product15']), headers=headers)
    data = response.json
    assert response.status_code == 200
    assert data['message'] == expected_message


def test_admin_update_product_non_exist(client, authorize_admin):
    """admin should not be able to update a non existent product"""
    headers = authorize_admin
    expected_message = 'product with id does not exist'

    response = client.put('/api/v2/products/{:d}'.format(10), data=json.dumps(PRODUCTS['product15']), headers=headers)
    data = response.json
    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_update_product_category_non_exist(client, authorize_admin):
    """admin should not be able to update a product with non existing category"""
    headers = authorize_admin
    expected_message = 'category provided does not exist'

    response = client.put('/api/v2/products/{:d}'.format(5), data=json.dumps(PRODUCTS['product16']), headers=headers)
    data = response.json
    assert response.status_code == 404
    assert data['message'] == expected_message


def test_admin_remove_product(client, authorize_admin):
    """admin should be able to delete a product"""
    headers = authorize_admin
    client.post('/api/v2/products', data=json.dumps(PRODUCTS['product5']), headers=headers)
    expected_message = 'product deleted successfully'

    response = client.delete('/api/v2/products/{:d}'.format(5), headers=headers)
    data = response.json

    assert response.status_code == 200
    assert data['message'] == expected_message


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
    expected_message = 'no sales added yet'

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


def test_attendant_get_users(client, authorize_attendant):
    """attendant should not be able to get all users of system"""
    headers = authorize_attendant
    expected_message = 'only admin can view users of the system'
    response = client.get('/api/v2/users', headers=headers)
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_add_attendant(client, authorize_attendant):
    """attendant should not be able to create an attendant account"""
    headers = authorize_attendant
    expected_result = 'only admin can add users to the system'

    username = USERS['user4']['username']
    password = USERS['user4']['password']

    credentials = {
        'username': username,
        'password': password
    }

    response = client.post('/api/v2/users', data=json.dumps(credentials), headers=headers)
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == expected_result


def test_attendant_get_attendant(client, authorize_attendant):
    """attendant should not be able to create an attendant account"""
    headers = authorize_attendant
    expected_message = 'only admin can view a user account'

    response = client.get('/api/v2/users/{:d}'.format(3), headers=headers)
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_delete_attendant(client, authorize_attendant):
    """attendant should not be able to delete another attendant"""
    headers = authorize_attendant
    expected_message = 'only admin can delete a user'

    response = client.delete('/api/v2/users/{:d}'.format(3), headers=headers)
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_add_category(client, authorize_attendant):
    """attendant should not be able to add category"""
    headers = authorize_attendant
    expected_message = 'only an admin can add a category'

    response = client.post('/api/v2/categories',
                           data=json.dumps(CATEGORIES['category1']), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_get_category(client, authorize_attendant):
    """attendant should not be able to get a category"""
    headers = authorize_attendant
    expected_message = 'only an admin can view categories'

    response = client.get('/api/v2/categories/{:d}'.format(1), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_get_categories(client, authorize_attendant):
    """attendant should not be able to get all categories"""
    headers = authorize_attendant

    expected_message = 'only an admin can view categories'
    response = client.get('/api/v2/categories', headers=headers)
    data = response.json

    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_update_category(client, authorize_attendant):
    """attendant should not be able to get a category"""
    headers = authorize_attendant
    expected_message = 'only an admin can update a category'

    response = client.put('/api/v2/categories/2', data=json.dumps(UPDATED_CATEGORY),
                          headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data['message'] == expected_message


def test_attendant_delete_category(client, authorize_attendant):
    """attendant should not be able to delete a category"""
    headers = authorize_attendant
    expected_message = 'only an admin can delete a category'
    response = client.delete('/api/v2/categories/{:d}'.format(3), headers=headers)
    data = response.get_json()
    assert response.status_code == 401
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
        'name': 'television',
        'description': 'a very cool television',
        'price': 30000,
        'category': 'electronics',
        'stock': 200,
        'min_stock': 20
    }

    response = client.get('/api/v2/products/{:d}'.format(3), headers=headers)
    data = response.json

    assert response.status_code == 200
    assert data['product'] == expected_result


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


def test_attendant_add_sale_excess(client, authorize_attendant):
    """attendant should not be able to sell more than available products"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale7']), headers=headers)
    data = response.json
    expected_response = 'failed to create sale record'
    assert response.status_code == 400
    assert data['message'] == expected_response


def test_attendant_add_sale_negative(client, authorize_attendant):
    """attendant should not be able to create sale with count of negative"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale3']), headers=headers)
    data = response.json
    expected_response = 'product count cannot be negative'
    assert response.status_code == 400
    assert data['message'] == expected_response


def test_attendant_add_sale_zero(client, authorize_attendant):
    """attendant should not be able to create sale with count of 0"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale4']), headers=headers)
    data = response.json
    expected_response = 'product count must be 1 and above'
    assert response.status_code == 400
    assert data['message'] == expected_response


def test_attendant_add_sale_non_existent(client, authorize_attendant):
    """attendant should not be able to sell product that doesn't exist"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale5']), headers=headers)
    data = response.json
    expected_response = 'failed to create sale record'
    assert response.status_code == 400
    assert data['message'] == expected_response


def test_attendant_add_sale_number(client, authorize_attendant):
    """attendant should not be able to sell product name which is only numbers"""
    headers = authorize_attendant
    response = client.post('/api/v2/sales', data=json.dumps(SALE_RECORDS['sale6']), headers=headers)
    data = response.json
    expected_response = 'name cannot be an integer value'
    assert response.status_code == 400
    assert data['message'] == expected_response


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
                "name": "table",
                "price": 10000,
                "quantity": 2,
                "cost": 20000
            },
            "2": {
                "name": "phone",
                "price": 20000,
                "quantity": 2,
                "cost": 40000
            },
            "3": {
                "name": "couch",
                "price": 50000,
                "quantity": 10,
                "cost": 500000
            }
        },
        "items": 14,
        "total": 560000,
        "attendant_id": 4
    }

    response = client.get('/api/v2/sales/{:d}'.format(2), headers=headers)

    data = response.json

    assert response.status_code == 200
    assert data == expected_result


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
                "name": "table",
                "price": 10000,
                "quantity": 2,
                "cost": 20000
            },
            "2": {
                "name": "phone",
                "price": 20000,
                "quantity": 2,
                "cost": 40000
            },
            "3": {
                "name": "couch",
                "price": 50000,
                "quantity": 10,
                "cost": 500000
            }
        },
        "items": 14,
        "total": 560000,
        "attendant_id": 4
    }

    response = client.get('/api/v2/sales/{:d}'.format(2), headers=headers)

    data = response.json

    assert response.status_code == 200
    assert data == expected_result
