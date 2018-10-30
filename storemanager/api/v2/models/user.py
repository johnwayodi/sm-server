"""This module contains the User model"""

from .abstract_model import AbstractModel


class UserModel(AbstractModel):
    """
    Model class for User.
    """

    def __init__(self):
        """ User has to have a username, password and a role."""
        super().__init__()
        self.username = str
        self.password = str
        self.role = str

    def save(self, statement, values):
        """Adds a new user"""
        return super().save(statement, values)

    def delete(self, statement, value):
        """deletes a user"""
        return super().delete(statement, value)

    def update(self, statement, values):
        """updates details of an existing user"""
        return super().update(statement, values)

    def as_dict(self):
        """Converts User to dict() object."""
        return {'id': self.id,
                'username': self.username,
                'role': self.role}
