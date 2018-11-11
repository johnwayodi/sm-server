from flask import request, abort
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flasgger import swag_from

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.category import CategoryModel
from storemanager.api.v2.utils.validators import CustomValidator
from storemanager.api.v2.utils.custom_checks import *

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
    @swag_from('docs/category_get.yml')
    def get(self, category_id):
        check_user_admin()
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
    @swag_from('docs/category_put.yml')
    def put(self, category_id):
        check_user_admin()
        check_id_integer(category_id)
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
    @swag_from('docs/category_delete.yml')
    def delete(self, category_id):
        check_user_admin()
        check_id_integer(category_id)

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
    @swag_from('docs/category_get_all.yml')
    def get(self):
        check_user_admin()
        categories = []
        result = CategoryModel.get_all(GET_ALL_CATEGORIES)

        for i in range(len(result)):
            category = CategoryModel()
            category.id = result[i][0]
            category.name = result[i][1]
            category.description = result[i][2]
            categories.append(category.as_dict())
        if not categories:
            return {'message': 'no categories added yet'}, 404
        return {'categories': categories}, 200

    @jwt_required
    @expects_json(CATEGORY_SCHEMA)
    @swag_from('docs/category_post.yml')
    def post(self):
        check_user_admin()
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
