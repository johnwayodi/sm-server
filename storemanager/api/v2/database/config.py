import os


def config():
    database = {
        'host': os.environ.get('DATABASE_HOST'),
        'database': os.environ.get('DATABASE_NAME'),
        'user': os.environ.get('DATABASE_USER'),
        'password': os.environ.get('DATABASE_PASS')
    }

    return database
