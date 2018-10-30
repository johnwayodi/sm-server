from .abstract_model import AbstractModel


class CategoryModel(AbstractModel):

    def __init__(self):
        super().__init__()
        self.name = str
        self.description = str

    def save(self, statement, values):
        """adds a new category to the categories table"""
        return super().save(statement, values)

    @classmethod
    def get_by_id(cls, statement, value):
        """retrieves one category with the specified id"""
        return super().get_by_id(statement, value)

    def delete(self, statement, value):
        """deletes a category from the categories table"""
        return super().delete(statement, value)

    def update(self, statement, values):
        """updates details of an existing category"""
        return super().update(statement, values)

    @classmethod
    def get_by_name(cls, statement, value):
        return super().get_by_name(statement, value)

    @classmethod
    def get_all(cls, statement):
        """retrieves all categories"""
        return super().get_all(statement)

    def as_dict(self):
        """Converts Category to dict() object."""
        return {'id': self.id,
                'name': self.name,
                'description': self.description
                }
