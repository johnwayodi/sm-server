from flask import request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.schemas import USER_LOGIN_SCHEMA, USER_REGISTRATION_SCHEMA
from storemanager.api.v2.models.user import UserModel


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
        if user_details[3] == "admin":
            if u_id.isdigit():
                result = UserModel.get_by_id(GET_USER, (u_id,))
                if result == {}:
                    return {'message': 'user with id does not exist'}, 404

                return {'message': 'user deleted successfully'}, 200

            return {'message': 'user id must be integer'}, 400

        return {'message': 'only admin can delete a User'}, 403


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

        return {'message': 'only admin can view users of the system'}


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

        # validation checks for username
        if isinstance(username, (int, float)):
            return {'message': 'username cannot be an integer value'}, 400
        if not username or username.isspace():
            return {
                       'message': 'username required should not be empty'
                   }, 400

        # validation checks for password
        if not password or password.isspace():
            return {'message': 'password is required, should not be empty'}, 400

        # validation checks for product name
        if isinstance(role, (int, float)):
            return {'message': 'user role cannot be an integer value'}, 400
        if not role or role.isspace():
            return {'message': 'user role required, should not be empty'}, 400

        if data['role'] == 'admin' or data['role'] == 'attendant':
            user_result = UserModel.get_by_name(GET_USER_BY_NAME, (username,))
            if user_result is not None:
                return {'message': 'User already exists'}, 400

            user = UserModel()
            saved_user = user.save(CREATE_USER, (username, password, role))
            user.id = saved_user[0]
            user.username = saved_user[1]
            user.role = saved_user[2]
            return {'message': 'user created',
                    'user': user.as_dict()}, 201

        return {'message': 'user role must be either admin or attendant'}, 400


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

        # validation checks for username
        if isinstance(username, (int, float)):
            return {'message': 'username cannot be an integer value'}, 400
        if not username or username.isspace():
            return {'message': 'username required should not be empty'}, 400

        # validation checks for password
        if not password or password.isspace():
            return {'message': 'password is required, should not be empty'}, 400

        user_result = UserModel.get_by_name(GET_USER_BY_NAME, (username,))
        if user_result is None:
            return {'message': 'user does not exist'}, 404

        if user_result[1] == username and user_result[2] == password:
            access_token = create_access_token(identity=username)
            return {'message': 'login successful',
                    'access_token': access_token}, 200

        if user_result[1] == username and user_result[2] != password:
            return {'message': 'wrong username or password, Try Again'}, 400