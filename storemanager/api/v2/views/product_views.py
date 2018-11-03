from flask import request
from flask_expects_json import expects_json
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.category import CategoryModel
from storemanager.api.v2.models.product import ProductModel
from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.models.schemas import PRODUCT_SCHEMA


class Product(Resource):
    """Allows requests on a single product"""

    @jwt_required
    def get(self, product_id):
        """
       Retrieve a Product
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
           name: p_id
           type: string
           required: true
           description: The Product Id
       responses:
         200:
           description: Success, Product Deleted
         403:
           description: Forbidden, Attendant can not delete Product
         400:
           description: Returned when value passed in as
            product_id is not an integer.
            """
        if product_id.isdigit():
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
        else:
            return {'message': 'product id must be integer'}, 400

    @jwt_required
    def put(self, product_id):
        """
       Updates a Product
       ---
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user
            login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
         - in: path
           name: p_id
           type: string
           required: true
           description: The Product Id
       responses:
         200:
           description: Product Deleted
         403:
           description: Forbidden, Attendant can not delete Product
         404:
           description: Product with specified id does not exist.
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if product_id.isdigit():
                data = request.get_json()
                name = data['name']
                description = data['description']
                price = data['price']
                stock = data['stock']
                min_stock = data['min_stock']
                category = data['category']

                category_details = CategoryModel.get_by_name(
                    GET_CATEGORY_BY_NAME, (category,))
                if category_details is None:
                    return {'message': 'category provided does not exist'}, 404
                category_id = category_details[0]

                result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
                if result is None:
                    return {'message': 'product with id does not exist'}, 404

                product = ProductModel()
                product.id = result[0]
                values = (name, description, price, stock,
                          min_stock, category_id, product.id)
                product.update(UPDATE_PRODUCT, values)
                return {'message': 'product updated successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400

        return {'message': 'only administrator can delete a product'}, 403

    @jwt_required
    def delete(self, product_id):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if product_id.isdigit():
                result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
                if result is None:
                    return {'message': 'product with id does not exist'}, 404

                product = ProductModel()
                product.id = result[0]
                product.delete(DELETE_PRODUCT, (product_id,))
                return {'message': 'product deleted successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400

        return {'message': 'only administrator can delete a product'}, 403


class ProductList(Resource):
    """Allows requests on products"""

    @jwt_required
    def get(self):
        """
       Get All Products
       ---
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user
            login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
       responses:
         200:
           description: Successful
         404:
           description: No products added to system yet
         422:
           description: Bad Authorization Error, Ensure jwt key is
            in the proper format in header.
            """
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
    def post(self):
        """
            Add New Product
           ---
           consumes:
             - application/json
           parameters:
             - in: header
               name: Authorization
               description: The jwt token generated during user
                login example (Bearer eyGssads...)
               type: string
               required: true
               default: Bearer token
             - in: body
               name: Product Details
               description: The Product to be added to Inventory
               schema:
                 type: object
                 required:
                   - name
                   - price
                   - description
                   - category
                   - stock
                   - min_stock
                 properties:
                    name:
                      type: string
                    price:
                      type: integer
                    description:
                      type: string
                    category:
                      type: string
                    stock:
                      type: integer
                    min_stock:
                      type: integer
           responses:
             200:
               description: The Product has been added successfully
             403:
               description: Admin user cannot create Sale Record
             400:
               description: Handles all Validation Errors
            """
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            data = request.get_json()
            product_name = data['name']
            product_price = data['price']
            product_description = data['description']
            product_category = data['category']
            product_stock = data['stock']
            product_min_stock = data['min_stock']

            # validation checks for product name
            if product_name.isdigit():
                return {
                           'message': 'name cannot be an integer value'
                       }, 400
            if not product_name or product_name.isspace():
                return {'message': 'name should not be empty'}, 400

            # validation checks for product price
            if product_price < 0:
                return {
                           'message': 'price cannot be a negative or 0'
                       }, 400

            # validation checks for product description
            if product_description.isdigit():
                return {
                           'message': 'category cannot be an integer value'
                       }, 400
            if not product_description or product_description.isspace():
                return {'message': 'category should not be empty'}, 400

            # validation checks for product category
            if product_category.isdigit():
                return {'message': 'category cannot be an integer value'}, 400
            if not product_category or product_category.isspace():
                return {'message': 'category should not be empty'}, 400

            # validation checks for product stock
            if product_stock < 0:
                return {'message': 'stock cannot be a negative or 0'}, 400

            # validation checks for product minimum stock
            if product_min_stock < 0:
                return {'message': 'minimum cannot be a negative or 0'}, 400

            product = ProductModel.get_by_name(
                GET_PRODUCT_BY_NAME, (product_name,))
            if product is not None:
                return {'message': 'product already exists'}, 400
            category_result = CategoryModel.get_by_name(
                GET_CATEGORY_BY_NAME, (product_category,))
            if category_result is None:
                return {'message': 'category provided does not exist'}, 400

            category_id = category_result[0]

            product_values = (product_name, product_price,
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

        return {'message': 'only admin can add a product'}, 403