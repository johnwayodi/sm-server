"""
This module contains a fuction check_user_admin that checks whether the
current user who is accessing an endpoint has a role of admin.
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity

from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.database.queries import *
from storemanager.api.v2.database.database import execute_query


def check_user_admin():
    """check whether user is an admin"""
    current_user = get_jwt_identity()
    user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
    if user_details[3] != "admin":
        abort(401, 'action failed, user is not administrator')


def check_id_integer(entity_id):
    """check whether value passed in url is an integer"""
    if not entity_id.isdigit():
        abort(400, 'provided id is not an integer')


def check_admin_exists():
    """check whether user with role 'admin' already exists in database"""
    admin = execute_query([CHECK_ADMIN_EXISTS], "one_row_count")
    if admin is not None:
        abort(400, 'admin user already exists')


def is_token_revoked(token):
    """
    Checks whether the token passed in the authorization header
    is in the revoked tokens table
    """
    result = execute_query([CHECK_TOKEN_VALIDITY, (token,)], "one")
    if not result:
        return False

    return True
