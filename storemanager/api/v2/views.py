"""
This Module contains all resources than will be added to the api
"""
from flask import request
from flask_expects_json import expects_json
from flask_restful import Resource
from storemanager.api.v2.database.queries import *
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models.user import UserModel
from .models.product import ProductModel
from .models.category import CategoryModel
from .models.sale_record import SaleRecordModel, SaleRecordModelItem
from .models.schemas import *


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
           description: The jwt token generated during user login example (Bearer eyGssads...)
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
           description: Returned when value passed in as product_id is not an integer.
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

            category_details = CategoryModel.get_by_id(GET_CATEGORY, (result[6],))
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
           description: The jwt token generated during user login example (Bearer eyGssads...)
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

                category_details = CategoryModel.get_by_name(GET_CATEGORY_BY_NAME, (category,))
                if category_details is None:
                    return {'message': 'category provided does not exist'}, 404
                category_id = category_details[0]

                result = ProductModel.get_by_id(GET_PRODUCT, (product_id,))
                if result is None:
                    return {'message': 'product with id does not exist'}, 404

                product = ProductModel()
                product.id = result[0]
                values = (name, description, price, stock, min_stock, category_id, product.id)
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
           description: The jwt token generated during user login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
       responses:
         200:
           description: Successful
         404:
           description: No products added to system yet
         422:
           description: Bad Authorization Error, Ensure jwt key is in the proper format in header.
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

            category_details = CategoryModel.get_by_id(GET_CATEGORY, (result[i][6],))
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
               description: The jwt token generated during user login example (Bearer eyGssads...)
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
                return {'message': 'product name cannot be an integer value'}, 400
            if not product_name or product_name.isspace():
                return {'message': 'product name should not be empty'}, 400

            # validation checks for product price
            if product_price < 0:
                return {'message': 'product price cannot be a negative or 0'}, 400

            # validation checks for product description
            if product_description.isdigit():
                return {'message': 'product category cannot be an integer value'}, 400
            if not product_description or product_description.isspace():
                return {'message': 'product category should not be empty'}, 400

            # validation checks for product category
            if product_category.isdigit():
                return {'message': 'product category cannot be an integer value'}, 400
            if not product_category or product_category.isspace():
                return {'message': 'product category should not be empty'}, 400

            # validation checks for product stock
            if product_stock < 0:
                return {'message': 'product stock cannot be a negative or 0'}, 400

            # validation checks for product minimum stock
            if product_min_stock < 0:
                return {'message': 'product minimum cannot be a negative or 0'}, 400

            product = ProductModel.get_by_name(GET_PRODUCT_BY_NAME, (product_name,))
            if product is not None:
                return {'message': 'product already exists, consider updating attributes'}, 400
            category_result = CategoryModel.get_by_name(GET_CATEGORY_BY_NAME, (product_category,))
            if category_result is None:
                return {'message': 'category provided does not exist'}, 400

            category_id = category_result[0]

            product_values = (product_name, product_price, product_stock,
                              product_min_stock, product_description, category_id)

            product = ProductModel()
            result = product.save(CREATE_PRODUCT, product_values)
            product.id = result[0]
            product.name = result[1]
            product.description = result[2]
            product.price = result[3]
            product.stock = result[4]
            product.min_stock = result[5]

            category_details = CategoryModel.get_by_id(GET_CATEGORY, (result[6],))
            category_name = category_details[1]
            product.category = category_name

            return {'message': 'product created',
                    'product': product.as_dict()}, 201

        return {'message': 'only admin can add a product'}, 403


class SaleRecord(Resource):
    """Allows requests on a single sale"""

    @jwt_required
    def get(self, s_id):
        """
       Get a Single Sale Record
       ---
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
         - in: path
           name: s_id
           type: string
           required: true
           description: The Sale Record Id
       responses:
         200:
           description: Sale Record with specified id is returned successfully
         404:
           description: No sale record matches the id specified, hence not found
         400:
           description: Validation Error, Only an integer value can be accepted as valid
            """
        if s_id.isdigit():
            sale_details = SaleRecordModel.get_by_id(GET_SALE, (s_id,))
            if sale_details is None:
                return {'message': 'sale with given id does not exist'}, 404

            sale = SaleRecordModel()
            sale.id = sale_details[0]
            sale.items = sale_details[1]
            sale.total = sale_details[2]

            sale_products = SaleRecordModelItem.get_all_by_id(GET_SALE_ITEMS, (sale.id,))
            products = {}
            for i in range(len(sale_products)):
                product = {
                    'name': sale_products[i][0],
                    'price': sale_products[i][1],
                    'quantity': sale_products[i][2],
                    'cost': sale_products[i][3]}
                products[i + 1] = product

            return {'id': sale.id,
                    'products': products,
                    'items': sale.items,
                    'total': sale.total}, 200
        else:
            return {'message': 'sale id must be integer'}, 400


class SaleRecords(Resource):
    """Allows requests on sales"""

    @jwt_required
    def get(self):
        """
       Get all Sale Records
       ---
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
       responses:
         200:
           description: lists of sale records returned successfully
         404:
           description: empty, no sale record created yet
            """
        sales = {}
        result = SaleRecordModel.get_all(GET_ALL_SALES)

        for i in range(len(result)):
            sale = SaleRecordModel()
            sale.id = result[i][0]
            sale.items = result[i][1]
            sale.total = result[i][2]
            sales[i + 1] = sale.as_dict()
        if sales == {}:
            return {'message': 'no sales added yet'}, 404

        return {'sales': sales}, 200

    @jwt_required
    def post(self):
        """
       Create a Sale Record
       ---
       consumes:
         - application/json
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user login example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
         - in: body
           name: Sale Record Details
           description: The Sale Record to be Created, count is the number of units to be sold for the product
           schema:
             type: object
             required:
               - username
               - password
               - role
             properties:
                products:
                  type: object
                  properties:
                    1:
                      type: object
                      properties:
                        product_id:
                          type: integer
                        count:
                          type: integer
       responses:
         200:
           description: Sale Record Created Successfully
         403:
           description: Authorization error, displayed when Admin tries to create a sale record
            """

        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "attendant":
            data = request.get_json()
            total_cost = 0
            items_count = 0
            products = []
            # product = None

            items = data['products']

            for i in range(len(items)):
                cart_id = str(i + 1)
                product_name = items[cart_id]['name']
                product = ProductModel.get_by_name(GET_PRODUCT_BY_NAME, (product_name,))
                # return {'result': product}
                if product is None:
                    return {'message': 'failed to create sale record',
                            'reason': 'product named {} does not exist'.format(product_name)}, 400

                quantity_in_cart = items[cart_id].get('count')
                product_price = product[2]
                cost = product_price * quantity_in_cart
                if product[3] - quantity_in_cart < product[4]:
                    return {'message': 'failed to create sale record',
                            'reason': 'cannot sell past minimum stock for {}'.format(product_name)}, 400

                new_stock_value = product[3] - quantity_in_cart
                ProductModel.update_on_sale(UPDATE_PRODUCT_ON_SALE, (new_stock_value, product[0]))

                product_info = (product_name, product_price, quantity_in_cart, cost)

                products.append(product_info)

                total_cost += cost
                items_count += quantity_in_cart

            sale = SaleRecordModel()
            sale.items = items_count
            sale.total = total_cost
            result = sale.save(CREATE_SALE, (items_count, total_cost))
            sale.id = result[0]

            products_in_sale = []
            for i in range(len(products)):
                product = products[i]
                sale_item = product + (sale.id,)
                # tuple(product)
                products_in_sale.append(sale_item)
            sale_items = SaleRecordModelItem()
            sale_items.save(CREATE_SALE_ITEM, products_in_sale)
            return {'message': 'Sale Record created successfully',
                    'sale': sale.as_dict()}, 201

        return {'message': 'only attendants can create a sale record'}, 403


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
           description: The jwt token generated during user login example (Bearer eyGssads...)
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
            return {'message': 'username required should not be empty'}, 400

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

        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404
                else:
                    category = CategoryModel()
                    category.id = result[0]
                    category.name = result[1]
                    category.description = result[2]
                return {'message': 'category details',
                        'category': category.as_dict()}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can view categories'}

    @jwt_required
    def put(self, category_id):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404

                category = CategoryModel()
                category.id = result[0]
                category.update(UPDATE_CATEGORY, (name, description, category.id))
                return {'message': 'category updated successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can update a category'}

    @jwt_required
    def delete(self, category_id):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404

                category = CategoryModel()
                category.id = result[0]
                category.delete(DELETE_CATEGORY, (category_id,))
                return {'message': 'category deleted successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can delete a product'}


class Categories(Resource):
    """Allows crud on categories"""

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            categories = {}
            result = CategoryModel.get_all(GET_ALL_CATEGORIES)

            for i in range(len(result)):
                category = CategoryModel()
                category.id = result[i][0]
                category.name = result[i][1]
                category.description = result[i][2]
                categories[i + 1] = category.as_dict()
            if categories == {}:
                return {'message': 'no categories added yet'}
            return {'categories': categories}, 200
        return {'message': 'only an admin can view categories'}

    @jwt_required
    @expects_json(CATEGORY_SCHEMA)
    def post(self):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            if name.isdigit():
                return {'message': 'name cannot be an integer value'}, 400
            if description.isdigit():
                return {'message': 'description cannot be an integer value'}, 400

            category = CategoryModel()
            result = category.save(CREATE_CATEGORY, (name, description))

            category.id = result[0]
            category.name = result[1]
            category.description = result[2]
            return {'message': 'category created',
                    'category': category.as_dict()}, 201
        return {'message': 'only an admin can add a category'}
