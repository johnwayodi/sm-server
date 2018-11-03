import os
import psycopg2
from storemanager.api.v2.database.config import config
from .queries import *


class Database:

    def connect(self):

        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

        return conn

    @classmethod
    def create_all_tables(cls):
        print('Creating Tables')
        create_tables_query = [
            CREATE_TABLE_USERS,
            CREATE_TABLE_CATEGORIES,
            CREATE_TABLE_PRODUCTS,
            CREATE_TABLE_SALES,
            CREATE_TABLE_SALE_ITEMS
        ]

        conn = None
        for statement in create_tables_query:
            try:
                params = config()
                conn = psycopg2.connect(**params)
                # conn = DB.connect()
                cur = conn.cursor()
                cur.execute(statement)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    @classmethod
    def drop_tables(cls):
        print('Dropping Tables')
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(DROP_ALL_TABLES)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


DB = Database()
