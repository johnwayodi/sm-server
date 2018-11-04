"""
This module contains a fuction check_user_admin that checks whether the
current user who is accessing an endpoint has a role of admin.
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity

from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.database.queries import GET_USER_BY_NAME


def check_user_admin():
    """check whether user is an admin"""
    current_user = get_jwt_identity()
    user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
    if user_details[3] != "admin":
        abort(401, 'action failed, user is not administrator')
