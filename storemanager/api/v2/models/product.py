""" This module contains the Product model."""
import psycopg2
from storemanager.api.v2.database.config import config
from .abstract_model import AbstractModel


class ProductModel(AbstractModel):
    """Model class for Product."""

    def __init__(self):
        """Parameters name, price, description, category, stock, min_stock"""
        super().__init__()
        self.name = str
        self.description = str
        self.price = int
        self.category = int
        self.stock = int
        self.min_stock = int

    def save(self, statement, values):
        """Adds a new product"""
        return super().save(statement, values)

    def delete(self, statement, value):
        """deletes a product"""
        return super().delete(statement, value)

    def update(self, statement, values):
        """updates details of an existing product"""
        return super().update(statement, values)

    @classmethod
    def update_on_sale(cls, statement, values):
        """updates stock value of product after sale"""
        conn = None
        rows_updated = 0
        try:
            params = config()
            conn = psycopg2.connect(**params)
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

    def as_dict(self):
        """Converts Product to dict() object."""
        return {'id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description,
                'category': self.category,
                'stock': self.stock,
                'min_stock': self.min_stock}
