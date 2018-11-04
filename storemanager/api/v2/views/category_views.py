from flask import request, abort
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.category import CategoryModel
from storemanager.api.v2.utils.validators import CustomValidator
from storemanager.api.v2.utils.check_role import check_user_identity

CATEGORY_SCHEMA = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['name', 'description']
}


class Category(Resource):
    """Allows crud on single category object"""

    @jwt_required
    def get(self, category_id):
        """
       Retrieve a Single Category item
       ---
       parameters:
         - in: path
           name: category_id
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

        # current_user = get_jwt_identity()
        # user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if check_user_identity() != "admin":
            return {'message': 'only an admin can view categories'}, 401
        if not category_id.isdigit():
            return {'message': 'provided id is not an integer'}, 400
        result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
        if result is None:
            return {'message': 'category with id does not exist'}, 404

        category = CategoryModel()
        category.id = result[0]
        category.name = result[1]
        category.description = result[2]
        return {'message': 'category details',
                'category': category.as_dict()}, 200

    @jwt_required
    def put(self, category_id):
        # current_user = get_jwt_identity()
        # user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if check_user_identity() != "admin":
            return {'message': 'only an admin can update a category'}, 401
        if not category_id.isdigit():
            return {'message': 'provided id is not an integer'}, 400
        data = request.get_json()
        name = data.get('name')
        c_name = name.lower().strip()
        description = data.get('description')
        result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
        if result is None:
            return {'message': 'category with id does not exist'}, 404

        category = CategoryModel()
        category.id = result[0]
        category.update(UPDATE_CATEGORY,
                        (c_name, description, category.id))
        return {'message': 'category updated successfully'}, 200


    @jwt_required
    def delete(self, category_id):
        # current_user = get_jwt_identity()
        # user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if check_user_identity() != "admin":
            return {'message': 'only an admin can delete a category'}, 401
        if not category_id.isdigit():
            return {'message': 'provided id is not an integer'}, 400

        result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
        if result is None:
            return {'message': 'category with id does not exist'}, 404

        category = CategoryModel()
        category.id = result[0]
        category.delete(DELETE_CATEGORY, (category_id,))
        return {'message': 'category deleted successfully'}, 200


class Categories(Resource):
    """Allows crud on categories"""

    @jwt_required
    def get(self):
        # current_user = get_jwt_identity()
        # user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if check_user_identity() == "admin":
            categories = {}
            result = CategoryModel.get_all(GET_ALL_CATEGORIES)

            for i in range(len(result)):
                category = CategoryModel()
                category.id = result[i][0]
                category.name = result[i][1]
                category.description = result[i][2]
                categories[i + 1] = category.as_dict()
            if categories == {}:
                return {'message': 'no categories added yet'}, 404
            return {'categories': categories}, 200
        return {'message': 'only an admin can view categories'}, 401

    @jwt_required
    @expects_json(CATEGORY_SCHEMA)
    def post(self):
        # current_user = get_jwt_identity()
        # user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if check_user_identity() == "admin":
            data = request.get_json()
            category_name = data['name']
            description = data['description']

            c_name = category_name.lower().strip()
            CustomValidator.validate_category_details(c_name, description)

            category = CategoryModel.get_by_name(
                GET_CATEGORY_BY_NAME, (c_name,))
            if category is not None:
                abort(400, 'category already exists')
            category = CategoryModel()
            result = category.save(CREATE_CATEGORY, (c_name, description))

            category.id = result[0]
            category.name = result[1]
            category.description = result[2]
            return {'message': 'category created',
                    'category': category.as_dict()}, 201
        return {'message': 'only an admin can add a category'}, 401
