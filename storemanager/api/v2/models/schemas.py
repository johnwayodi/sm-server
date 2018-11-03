

CATEGORY_SCHEMA = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['name', 'description']
}

PRODUCT_SCHEMA = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'name': {'type': 'string'},
        'price': {'type': 'integer'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'stock': {'type': 'integer'},
        'min_stock': {'type': 'integer'},
    },
    'required': ['name', 'price', 'description',
                 'category', 'stock', 'min_stock']
}

USER_REGISTRATION_SCHEMA = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string'}
    },
    'required': ['username', 'password', 'role']
}

USER_LOGIN_SCHEMA = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}
