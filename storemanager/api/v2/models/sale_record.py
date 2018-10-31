""" This module contains the Sale Record model."""
import psycopg2
from storemanager.api.v2.database.config import config
from .abstract_model import AbstractModel


class SaleRecordModel(AbstractModel):
    """Model class for Sale Record."""

    def __init__(self):
        """ Parameters products, items and total cost. """
        super().__init__()
        self.items = int
        self.total = int

    def save(self, statement, values):
        """Adds a new sale record"""
        return super().save(statement, values)

    def delete(self, statement, value):
        """deletes a sale record"""
        return super().delete(statement, value)

    def as_dict(self):
        """Converts Sale Record to dict() object."""
        return {'id': self.id,
                'items': self.items,
                'total': self.total}


class SaleRecordModelItem(AbstractModel):
    def __init__(self):
        """ Parameters products, items and total cost. """
        super().__init__()
        self.product_name = str
        self.product_price = int
        self.product_quantity = int
        self.product_total = int
        self.sale_id = int

    def save(self, statement, values):
        """Adds a new sale item"""
        # return super().save(statement, values)
        conn = None
        # result_row = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.executemany(statement, values)
            # result_row = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        # return result_row

    def delete(self, statement, value):
        """deletes a sale item"""
        return super().delete(statement, value)

    def as_dict(self):
        """Converts Sale Item to dict() object."""
        return {'id': self.id,
                'products': self.product_price,
                'items': self.product_quantity,
                'total': self.product_total}
