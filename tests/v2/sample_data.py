MIMETYPE = 'application/json'
HEADERS = {
    'Content-Type': MIMETYPE,
    'Accept': MIMETYPE,
}

PRODUCTS = {
    "product1": {
        'name': 'Table',
        'price': 10000,
        'description': 'a cool table',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product2": {
        'name': 'Phone',
        'price': 20000,
        'description': 'a cool phone',
        'category': 'Electronics',
        'stock': 1000,
        'min_stock': 50
    },
    "product3": {
        'name': 'Television',
        'price': 30000,
        'description': 'a cool television',
        'category': 'Electronics',
        'stock': 200,
        'min_stock': 20
    },
    "product4": {
        'name': 'Couch',
        'price': 50000,
        'description': 'a cool couch',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product5": {
        'name': 'Bed',
        'price': 50000,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    }
}

CATEGORIES = {
    "category1": {
        "name": "Furniture",
        "description": "this is the furniture category"
    },
    "category2": {
        "name": "Electronics",
        "description": "this is the electronics category"
    },
    "category3": {
        "name": "Food",
        "description": "this is the Food category"
    },
    "category4": {
        "name": "Accessories",
        "description": "this is the Accessories category"
    }
}

UPDATED_CATEGORY = {
    "name": "Electronics",
    "description": "this is the updated electronics category"
}

SALE_RECORDS = {
    "sale1": {
        "products": {
            "1": {
                "name": "Table",
                "count": 2
            },
            "2": {
                "name": "Television",
                "count": 10
            }
        }
    },
    "sale2": {
        "products": {
            "1": {
                "name": "Table",
                "count": 2
            },
            "2": {
                'name': 'Phone',
                "count": 2
            },
            "3": {
                'name': 'Couch',
                "count": 10
            }
        }
    }
}

USERS = {
    "user1": {
        "username": "jack",
        "password": "tester",
        "role": "attendant"
    },
    "user2": {
        "username": "abraham",
        "password": "lincoln",
        "role": "admin"
    },
    "user3": {
        "username": "jacky",
        "password": "testerin",
        "role": "attendant"
    },
    "user4": {
        "username": "walulu",
        "password": "testiod",
        "role": "attendant"
    }

}
