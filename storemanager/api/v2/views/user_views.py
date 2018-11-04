from flask import request, abort
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, create_access_token, \
    get_jwt_identity
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.utils.validators import CustomValidator

USER_REGISTRATION_SCHEMA = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string'}
    },
    'required': ['username', 'password', 'role']
}

USER_LOGIN_SCHEMA = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}


class User(Resource):
    """Allows requests on single user"""

    @jwt_required
    def get(self, u_id):
        """
       Retrieve a User
       ---
       parameters:
         - in: path
           name: user_id
           type: string
           required: true
       responses:
         200:
           description: Displayed when user deleted successfully
         404:
           description: Displayed when no user is found with specified id
         403:
           description: Error shown to Attendant trying to delete product
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] != "admin":
            abort(401, 'only admin can view a user account')
        if u_id.isdigit():
            user_details = UserModel.get_by_id(GET_USER, (u_id,))
            if user_details is None:
                return {'message': 'user with id does not exist'}, 404

            user = UserModel()
            user.id = user_details[0]
            user.username = user_details[1]
            user.role = user_details[2]
            return {'user': user.as_dict()}, 200
        else:
            return {'message': 'user id must be integer'}, 400

    @jwt_required
    def delete(self, u_id):
        """
       Delete a User
       ---
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user login
            example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
         - in: path
           name: u_id
           type: integer
           required: true
       responses:
         200:
           description: User deleted successfully
         404:
           description: User with id does not exist
         403:
           description: Error for Attendant trying to delete product
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] != "admin":
            abort(401, 'only admin can delete a user')
        if not u_id.isdigit():
            abort(400, 'user id must be integer')
        result = UserModel.get_by_id(GET_USER, (u_id,))
        if result is not None:
            user = UserModel()
            user.delete(DELETE_USER, (u_id,))
            return {'message': 'user deleted successfully'}, 200

        return {'message': 'user with id does not exist'}, 404


class UserList(Resource):
    """Allow requests on users"""

    @jwt_required
    def get(self):
        """
       Retrieve All Users
       ---
       responses:
         200:
           description: List of Users Returned Successful
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            users = {}
            result = UserModel.get_all(GET_ALL_USERS)

            for i in range(len(result)):
                user = UserModel()
                user.id = result[i][0]
                user.username = result[i][1]
                user.role = result[i][2]
                users[i + 1] = user.as_dict()
            if users == {}:
                return {'message': 'no users in system yet'}, 404

            return {'users': users}, 200

        return {'message': 'only admin can view users of the system'}, 401

    @jwt_required
    def post(self):
        """
       Add a new User, can only add a User of type attendant.
       ---
       responses:
         200:
           description: List of Users Returned Successful
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            data = request.get_json()
            username = data['username']
            password = data['password']

            a_name = username.lower().strip()
            result = UserModel.get_by_name(GET_USER_BY_NAME, (a_name,))
            if result is None:
                user = UserModel()
                user.username = a_name
                user.password = password
                user.role = "attendant"
                user.save(CREATE_USER, (user.username, user.password, user.role))
                return {'message': 'attendant created successfully'}, 201

            abort(400, 'attendant with similar name exists')

        abort(401, 'only admin can add users to the system')


class UserRegistration(Resource):
    """Allows registration of users"""

    @expects_json(USER_REGISTRATION_SCHEMA)
    def post(self):
        """
       Register User
       ---
       consumes:
         - application/json
       parameters:
         - in: body
           name: Registration Details
           description: The User to be registered
           schema:
             type: object
             required:
               - username
               - password
               - role
             properties:
                username:
                  type: string
                  default: jack
                password:
                  type: string
                  default: ryan001
                role:
                  type: string
                  default: admin
       responses:
         200:
           description: User Created Successfully
         400:
           description: Validation Error
            """
        data = request.get_json()
        username = data['username']
        password = data['password']
        role = data['role']

        u_name = username.lower().strip()
        CustomValidator.validate_register_details(u_name, password, role)

        if data['role'] == 'admin' or data['role'] == 'attendant':
            user_result = UserModel.get_by_name(GET_USER_BY_NAME, (u_name,))
            if user_result is not None:
                return {'message': 'User already exists'}, 400

            user = UserModel()
            saved_user = user.save(CREATE_USER, (u_name, password, role))
            user.id = saved_user[0]
            user.username = saved_user[1]
            user.role = saved_user[2]
            return {'message': 'user created',
                    'user': user.as_dict()}, 201

        return {'message': 'user role must be admin or attendant'}, 400


class UserLogin(Resource):
    """Allows user who is registered to log in"""

    @expects_json(USER_LOGIN_SCHEMA)
    def post(self):
        """
       Login User
       ---
       consumes:
         - application/json
       parameters:
         - in: body
           name: Login Credentials
           description: The User to be Login
           schema:
             type: object
             required:
               - username
               - password
             properties:
                username:
                  type: string
                  default: Jack
                password:
                  type: string
                  default: ryan001
       responses:
         200:
           description: login successful
         404:
           description: User with that username does not exist
         400:
           description: Validation Error
            """

        data = request.get_json()
        username = data['username']
        password = data['password']

        uname = username.lower().strip()

        CustomValidator.validate_login_details(uname, password)

        user_result = UserModel.get_by_name(GET_USER_BY_NAME, (uname,))
        if user_result is None:
            return {'message': 'user does not exist'}, 404

        if user_result[1] == uname and user_result[2] == password:
            access_token = create_access_token(identity=uname)
            return {'message': 'login successful',
                    'access_token': access_token}, 200

        if user_result[1] == uname and user_result[2] != password:
            return {'message': 'wrong username or password, '
                               'Try Again'}, 400
