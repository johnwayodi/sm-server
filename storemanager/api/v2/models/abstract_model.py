"""
This module contains the Generic Model
UserModel, ProductModel and SaleRecordModel inherit from AbstractModel
"""
import psycopg2
from storemanager.api.v2.database.config import config
from storemanager.api.v2.database.database import DB


class AbstractModel:
    """ Model class for AbstractModel. """
    conn = None
    result_row = None

    def __init__(self):
        self.id = int

    def save(self, statement, values):
        """create a new item using the entity details specified"""
        # conn = None
        # result_row = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, values)
            result_row = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result_row

    @classmethod
    def get_by_id(cls, statement, value):
        """Retrieve the entity with the specified id"""
        conn = None
        result_row = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, value)
            result_row = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result_row

    def delete(self, statement, value):
        """Delete the entity with the specified id"""
        conn = None
        rows_deleted = 0
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, value)
            rows_deleted = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return rows_deleted

    def update(self, statement, values):
        """Update the entity with the specified id"""
        conn = None
        rows_updated = 0
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, values)
            rows_updated = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return rows_updated

    @classmethod
    def get_all(cls, statement):
        """Returns multiple rows of the type of entity"""
        conn = None
        result_rows = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement)
            result_rows = cur.fetchall()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result_rows

    @classmethod
    def get_all_by_id(cls, statement, values):
        """Returns all entities which contain the specified id"""
        conn = None
        result_rows = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, values)
            result_rows = cur.fetchall()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result_rows

    @classmethod
    def get_by_name(cls, statement, value):
        """Returns the entity with the specified name"""
        conn = None
        result_row = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            # conn = DB.connect()
            cur = conn.cursor()
            cur.execute(statement, value)
            result_row = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result_row
