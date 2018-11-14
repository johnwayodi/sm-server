"""
This module contains the Generic Model
UserModel, ProductModel and SaleRecordModel inherit from AbstractModel
"""
from storemanager.api.v2.database.database import execute_query


class AbstractModel:
    """ Model class for AbstractModel. """

    def __init__(self):
        self.id = int
        self.created = str

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
