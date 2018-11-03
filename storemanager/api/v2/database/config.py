"""
This module contains the config function which contains a dictionary.
The dictionary contains the database connection information.
"""
import os


def config():
    """Database configurations for use with local database instance"""
    database = {
        'host': os.environ.get('DATABASE_HOST'),
        'database': os.environ.get('DATABASE_NAME'),
        'user': os.environ.get('DATABASE_USER'),
        'password': os.environ.get('DATABASE_PASS')
    }

    return database
