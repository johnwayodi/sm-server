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
    },
    "product6": {
        'name': '12345',
        'price': 50000,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product7": {
        'name': '  ',
        'price': 50000,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product8": {
        'name': 'King size Bed',
        'price': -500,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product9": {
        'name': 'Double Desker',
        'price': 500,
        'description': '123456',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': 10
    },
    "product10": {
        'name': 'Desk',
        'price': 500,
        'description': 'a cool bed',
        'category': '12345',
        'stock': 100,
        'min_stock': 10
    },
    "product11": {
        'name': 'Desk',
        'price': 500,
        'description': '  ',
        'category': '12345',
        'stock': 100,
        'min_stock': 10
    },
    "product12": {
        'name': 'Desk',
        'price': 500,
        'description': 'a cool bed',
        'category': '  ',
        'stock': 100,
        'min_stock': 10
    },
    "product13": {
        'name': 'Desk',
        'price': 500,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': -100,
        'min_stock': 10
    },
    "product14": {
        'name': 'Desk',
        'price': 500,
        'description': 'a cool bed',
        'category': 'Furniture',
        'stock': 100,
        'min_stock': -10
    },
    "product15": {
        'name': 'Television',
        'price': 30000,
        'description': 'a very cool television',
        'category': 'electronics',
        'stock': 200,
        'min_stock': 20
    },
    "product16": {
        'name': 'Bed',
        'price': 50000,
        'description': 'a updated cool bed',
        'category': 'Fashion',
        'stock': 1000,
        'min_stock': 100
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
    },
    "category5": {
        "name": "12345",
        "description": "this is the electronics category"
    },
    "category6": {
        "name": " ",
        "description": "this is the electronics category"
    },
    "category7": {
        "name": "Home",
        "description": "123456"
    }
}

UPDATED_CATEGORY = {
    "name": "Electronics",
    "description": "this is the updated electronics category"
}

SALE_RECORDS = {
    "sale1": {
        "products": [
            {
                "name": "Table",
                "count": 2
            },
            {
                "name": "Television",
                "count": 10
            }
        ]
    },
    "sale2": {
        "products": [
            {
                "name": "Table",
                "count": 2
            },
            {
                'name': 'Phone',
                "count": 2
            },
            {
                'name': 'Couch',
                "count": 10
            }
        ]
    },
    "sale3": {
        "products": [
            {
                "name": "Table",
                "count": -2
            }
        ]
    },
    "sale4": {
        "products": [
            {
                "name": "Table",
                "count": 0
            }
        ]
    },
    "sale5": {
        "products": [
            {
                "name": "Chocolate",
                "count": 10
            }
        ]
    },
    "sale6": {
        "products": [
            {
                "name": "1234",
                "count": 10
            }
        ]
    },
    "sale7": {
        "products": [
            {
                "name": "Table",
                "count": 100000
            }
        ]
    }
}

USERS = {
    "user1": {
        "username": "jack",
        "password": "tester"
    },
    "user2": {
        "username": "abraham",
        "password": "lincoln"
    },
    "user3": {
        "username": "jacky",
        "password": "testerin"
    },
    "user4": {
        "username": "walulu",
        "password": "testiod"
    }

}
