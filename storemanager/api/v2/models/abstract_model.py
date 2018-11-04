"""
This module contains the Generic Model
UserModel, ProductModel and SaleRecordModel inherit from AbstractModel
"""
import psycopg2
from storemanager.api.v2.database.database import DB

conn = None
result = None


class AbstractModel:
    """ Model class for AbstractModel. """

    def __init__(self):
        self.id = int

    def save(self, statement, values):
        """create a new item using the entity details specified"""
        return execute_query([statement, values], "one")

    @classmethod
    def get_by_id(cls, statement, value):
        """Retrieve the entity with the specified id"""
        return execute_query([statement, value], "one")

    def delete(self, statement, value):
        """Delete the entity with the specified id"""
        return execute_query([statement, value], "one_row_count")

    def update(self, statement, values):
        """Update the entity with the specified id"""
        return execute_query([statement, values], "one_row_count")

    @classmethod
    def get_all(cls, statement):
        """Returns multiple rows of the type of entity"""
        return execute_query([statement], "many_no_values")

    @classmethod
    def get_one(cls, statement):
        """Returns one row result"""
        return execute_query([statement], "one")

    @classmethod
    def get_all_by_id(cls, statement, values):
        """Returns all entities which contain the specified id"""
        return execute_query([statement, values], "many")

    @classmethod
    def get_by_name(cls, statement, value):
        """Returns the entity with the specified name"""
        return execute_query([statement, value], "one")


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
