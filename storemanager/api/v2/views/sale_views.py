from flask import request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.product import ProductModel
from storemanager.api.v2.models.sale_record import *
from storemanager.api.v2.models.user import UserModel
from storemanager.api.v2.utils.validators import CustomValidator
from storemanager.api.v2.utils.custom_checks import check_id_integer

SALES_SCHEMA = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "count": {"type": "integer"}
                },
                "required": ["name", "count"]
            }
        }
    },
    "required": [
        "products"
    ]
}


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
           description: The jwt token generated during
            user login example (Bearer eyGssads...)
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
           description: Sale Record with specified id is
            returned successfully
         404:
           description: No sale record matches the id specified,
            hence not found
         400:
           description: Validation Error, Only an integer value
            can be accepted as valid
            """
        check_id_integer(s_id)
        sale_details = SaleRecordModel.get_by_id(GET_SALE, (s_id,))
        if sale_details is None:
            return {'message': 'sale with given id does not exist'}, 404

        sale = SaleRecordModel()
        sale.id = sale_details[0]
        sale.items = sale_details[1]
        sale.total = sale_details[2]
        sale.attendant = sale_details[3]
        sale_products = SaleRecordModelItem.get_all_by_id(
            GET_SALE_ITEMS, (sale.id,))
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
                'total': sale.total,
                'attendant_id': sale.attendant}, 200


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
           description: The jwt token generated during user
            login example (Bearer eyGssads...)
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
            sale.attendant = result[i][3]
            sales[i + 1] = sale.as_dict()
        if sales == {}:
            return {'message': 'no sales added yet'}, 404

        return {'sales': sales}, 200

    @jwt_required
    @expects_json(SALES_SCHEMA)
    def post(self):
        """
       Create a Sale Record
       ---
       consumes:
         - application/json
       parameters:
         - in: header
           name: Authorization
           description: The jwt token generated during user login
            example (Bearer eyGssads...)
           type: string
           required: true
           default: Bearer token
         - in: body
           name: Sale Record Details
           description: The Sale Record to be Created, count is the
            number of units to be sold for the product
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
           description: Authorization error, displayed when
            Admin tries to create a sale record
            """

        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "attendant":
            data = request.get_json()
            total_cost = 0
            items_count = 0
            products = []

            items = data['products']

            for i in range(len(items)):
                product_name = items[i]['name']
                quantity_in_cart = items[i]['count']

                p_name = product_name.lower().strip()

                CustomValidator.validate_sale_items(
                    p_name, quantity_in_cart)

                product = ProductModel.get_by_name(
                    GET_PRODUCT_BY_NAME, (p_name,))
                if product is None:
                    return {'message': 'failed to create sale record',
                            'reason': 'product named {} does '
                                      'not exist'.format(p_name)}, 400

                product_price = product[2]
                cost = product_price * quantity_in_cart
                if product[3] - quantity_in_cart < product[4]:
                    return {'message': 'failed to create sale record',
                            'reason': 'cannot sell past minimum '
                                      'stock for {}'.format(p_name)}, 400

                new_stock_value = product[3] - quantity_in_cart
                ProductModel.update_on_sale(
                    UPDATE_PRODUCT_ON_SALE, (new_stock_value, product[0]))

                product_info = (p_name,
                                product_price,
                                quantity_in_cart,
                                cost)

                products.append(product_info)

                total_cost += cost
                items_count += quantity_in_cart

            attendant_id = user_details[0]

            sale = SaleRecordModel()
            sale.items = items_count
            sale.total = total_cost
            sale.attendant = attendant_id
            result = sale.save(CREATE_SALE, (items_count, total_cost, attendant_id))
            sale.id = result[0]

            products_in_sale = []
            for i in range(len(products)):
                product = products[i]
                sale_item = product + (sale.id,)
                tuple(product)
                products_in_sale.append(sale_item)
            sale_items = SaleRecordModelItem()
            sale_items.save(CREATE_SALE_ITEM, products_in_sale)
            return {'message': 'Sale Record created successfully',
                    'sale': sale.as_dict()}, 201

        return {'message': 'only attendants can create a sale record'}, 403
