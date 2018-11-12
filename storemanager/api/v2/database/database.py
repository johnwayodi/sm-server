import os
import psycopg2
from storemanager.api.v2.database.config import config
from .queries import *

conn = None
result = None


class Database:

    def connect(self):
        params = config()
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

        return conn

    @classmethod
    def create_all_tables(cls):
        print('Creating Tables')
        create_tables_query = [
            CREATE_TABLE_USERS,
            CREATE_TABLE_CATEGORIES,
            CREATE_TABLE_PRODUCTS,
            CREATE_TABLE_SALES,
            CREATE_TABLE_SALE_ITEMS,
            CREATE_TOKENS_TABLE
        ]

        for statement in create_tables_query:
            execute_query([statement], "one_no_result")

    @classmethod
    def drop_tables(cls):
        print('Dropping Tables')
        execute_query([DROP_ALL_TABLES], "one_no_result")


def execute_query(query, flag):
    """Execute queries based on flag values"""
    try:
        global conn, result
        statement = query[0]
        conn = DB.connect()
        cur = conn.cursor()

        if flag is "one":
            values = query[1]
            cur.execute(statement, values)
            result = cur.fetchone()

        elif flag is "one_no_result":
            cur.execute(statement)
        elif flag is "many":
            values = query[1]
            cur.execute(statement, values)
            result = cur.fetchall()

        elif flag is "many_no_values":
            cur.execute(statement)
            result = cur.fetchall()

        elif flag is "one_row_count":
            value = query[1]
            cur.execute(statement, value)
            result = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result


DB = Database()
