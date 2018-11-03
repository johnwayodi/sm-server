"""
This module contains the Generic Model
UserModel, ProductModel and SaleRecordModel inherit from AbstractModel
"""
import psycopg2
from storemanager.api.v2.database.config import config
from storemanager.api.v2.database.database import DB

conn = None
result_row = None
rows_deleted = 0
rows_updated = 0


class AbstractModel:
    """ Model class for AbstractModel. """

    def __init__(self):
        self.id = int

    def save(self, statement, values):
        """create a new item using the entity details specified"""
        global conn, result_row
        try:
            conn = DB.connect()
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
        global conn, result_row
        try:
            conn = DB.connect()
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
        global conn, rows_deleted
        try:
            conn = DB.connect()
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
        global conn, rows_updated
        try:
            conn = DB.connect()
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
        global conn, result_rows
        try:
            conn = DB.connect()
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
        global conn, result_rows
        try:
            conn = DB.connect()
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
        global conn, result_row
        try:
            conn = DB.connect()
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
