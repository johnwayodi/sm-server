from flask_jwt_extended import get_jwt_identity

from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.database.queries import GET_USER_BY_NAME


def check_user_identity():
    current_user = get_jwt_identity()
    user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
    return user_details[3]
