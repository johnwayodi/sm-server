""" This module contains the Sale Record model."""
import psycopg2
from .abstract_model import AbstractModel
from storemanager.api.v2.database.database import DB


class SaleRecordModel(AbstractModel):
    """Model class for Sale Record."""

    def __init__(self):
        """ Parameters products, items and total cost. """
        super().__init__()
        self.items = int
        self.total = int
        self.attendant = int

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
                'total': self.total,
                'attendant_id': self.attendant}


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
        conn = None
        try:
            conn = DB.connect()
            cur = conn.cursor()
            cur.executemany(statement, values)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def delete(self, statement, value):
        """deletes a sale item"""
        return super().delete(statement, value)

    def as_dict(self):
        """Converts Sale Item to dict() object."""
        return {'id': self.id,
                'products': self.product_price,
                'items': self.product_quantity,
                'total': self.product_total}
