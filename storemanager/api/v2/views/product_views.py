from flask import request, abort
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flasgger import swag_from

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.category import CategoryModel
from storemanager.api.v2.models.product import ProductModel
from storemanager.api.v2.utils.validators import CustomValidator
from storemanager.api.v2.utils.custom_checks import *

PRODUCT_SCHEMA = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'name': {'type': 'string'},
        'price': {'type': 'integer'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'stock': {'type': 'integer'},
        'min_stock': {'type': 'integer'},
    },
    'required': ['name', 'price', 'description',
                 'category', 'stock', 'min_stock']
}


class Product(Resource):
    """Allows requests on a single product"""

    @jwt_required
    @swag_from('docs/product_get.yml')
    def get(self, product_id):
        """get one product"""
        check_id_integer(product_id)
        result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
        if result is None:
            return {'message': 'product with id does not exist'}, 404

        product = ProductModel()
        product.id = result[0]
        product.name = result[1]
        product.price = result[2]
        product.stock = result[3]
        product.min_stock = result[4]
        product.description = result[5]

        category_details = CategoryModel.get_by_id(
            GET_CATEGORY, (result[6],))
        category_name = category_details[1]
        product.category = category_name

        return {'product': product.as_dict()}, 200

    @jwt_required
    @swag_from('docs/product_put.yml')
    def put(self, product_id):
        """update a product"""
        check_user_admin()
        check_id_integer(product_id)
        data = request.get_json()
        name = data['name']
        description = data['description']
        price = data['price']
        stock = data['stock']
        min_stock = data['min_stock']
        category = data['category']

        p_name = name.lower().strip()
        p_cat = category.lower().strip()
        category_details = CategoryModel.get_by_name(
            GET_CATEGORY_BY_NAME, (p_cat,))
        if category_details is None:
            return {'message': 'category provided does not exist'}, 404
        category_id = category_details[0]

        result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
        if result is None:
            return {'message': 'product with id does not exist'}, 404

        product = ProductModel()
        product.id = result[0]
        values = (p_name, description, price, stock,
                  min_stock, category_id, product.id)
        product.update(UPDATE_PRODUCT, values)
        return {'message': 'product updated successfully'}, 200

    @jwt_required
    @swag_from('docs/product_delete.yml')
    def delete(self, product_id):
        """delete a product"""
        check_user_admin()
        check_id_integer(product_id)
        result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
        if result is None:
            return {'message': 'product with id does not exist'}, 404

        product = ProductModel()
        product.id = result[0]
        product.delete(DELETE_PRODUCT, (product_id,))
        return {'message': 'product deleted successfully'}, 200


class ProductList(Resource):
    """Allows requests on products"""

    @jwt_required
    @swag_from('docs/product_get_all.yml')
    def get(self):
        """get all products"""
        products = {}
        result = ProductModel.get_all(GET_ALL_PRODUCTS)
        for i in range(len(result)):
            product = ProductModel()
            product.id = result[i][0]
            product.name = result[i][1]
            product.price = result[i][2]
            product.stock = result[i][3]
            product.min_stock = result[i][4]
            product.description = result[i][5]

            category_details = CategoryModel.get_by_id(
                GET_CATEGORY, (result[i][6],))
            category_name = category_details[1]

            product.category = category_name
            products[i + 1] = product.as_dict()
        if products == {}:
            return {'message': 'no products added yet'}, 404

        return {'products': products}, 200

    @jwt_required
    @expects_json(PRODUCT_SCHEMA)
    @swag_from('docs/product_post.yml')
    def post(self):
        """add a new product"""
        check_user_admin()
        data = request.get_json()
        product_name = data['name']
        product_price = data['price']
        product_description = data['description']
        product_category = data['category']
        product_stock = data['stock']
        product_min_stock = data['min_stock']

        p_name = product_name.lower().strip()
        p_cat = product_category.lower().strip()

        CustomValidator.validate_product_details(
            p_name, product_price, product_description,
            p_cat, product_stock, product_min_stock
        )

        product = ProductModel.get_by_name(
            GET_PRODUCT_BY_NAME, (p_name,))
        if product is not None:
            return {'message': 'product already exists'}, 400
        category_result = CategoryModel.get_by_name(
            GET_CATEGORY_BY_NAME, (p_cat,))
        if category_result is None:
            return {'message': 'category provided does not exist'}, 400

        category_id = category_result[0]

        product_values = (p_name, product_price,
                          product_stock, product_min_stock,
                          product_description, category_id)

        product = ProductModel()
        result = product.save(CREATE_PRODUCT, product_values)
        product.id = result[0]
        product.name = result[1]
        product.description = result[2]
        product.price = result[3]
        product.stock = result[4]
        product.min_stock = result[5]

        category_details = CategoryModel.get_by_id(
            GET_CATEGORY, (result[6],))
        category_name = category_details[1]
        product.category = category_name

        return {'message': 'product created',
                'product': product.as_dict()}, 201
