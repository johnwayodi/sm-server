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
        'category': 'furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product2": {
        'name': 'Phone',
        'price': 20000,
        'description': 'a cool phone',
        'category': 'smart phone',
        'stock': 1000,
        'min_stock': 50
    },
    "product3": {
        'name': 'Television',
        'price': 30000,
        'description': 'a cool television',
        'category': 'electronic',
        'stock': 200,
        'min_stock': 20
    },
    "product4": {
        'name': 'Couch',
        'price': 50000,
        'description': 'a cool couch',
        'category': 'furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product5": {
        'name': 'Android',
        'price': 5000,
        'description': 'a cool phone',
        'category': 'Phone',
        'stock': 100,
        'min_stock': 10
    }
}

SALE_RECORDS = {
    "sale1": {
        "products": {
            "1": {
                "product_id": 1,
                "count": 2
            },
            "2": {
                "product_id": 3,
                "count": 10
            }
        }
    },
    "sale2": {
        "products": {
            "1": {
                "product_id": 1,
                "count": 2
            },
            "2": {
                "product_id": 2,
                "count": 2
            },
            "3": {
                "product_id": 4,
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
