""" This module contains the Product model."""
from .abstract_model import AbstractModel
from storemanager.api.v2.database.database import execute_query


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
        execute_query([statement, values], "one_row_count")

    def as_dict(self):
        """Converts Product to dict() object."""
        return {'id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description,
                'category': self.category,
                'stock': self.stock,
                'min_stock': self.min_stock,
                'date_created': self.created}
