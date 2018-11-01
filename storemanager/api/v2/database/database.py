import os
import psycopg2
from storemanager.api.v2.database.config import config
from flask import current_app
from .queries import create_table_users, create_table_products, create_table_categories, \
    create_table_sales, create_table_sale_items, drop_all_tables


class Database:

    def connect(self):

        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

        return conn

    @classmethod
    def create_all_tables(cls):
        create_tables_query = [
            create_table_users,
            create_table_categories,
            create_table_products,
            create_table_sales,
            create_table_sale_items
        ]

        conn = None
        for statement in create_tables_query:
            try:
                params = config()
                conn = psycopg2.connect(**params)
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

        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(drop_all_tables)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
