from flask import Blueprint
from flask_restful import Api
from storemanager.api.v2.views import *

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v2")
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

api = Api(api_blueprint)
auth_api = Api(auth_blueprint)

api.add_resource(ProductList, '/products')
api.add_resource(Product, '/products/<product_id>')

api.add_resource(SaleRecords, '/sales')
api.add_resource(SaleRecord, '/sales/<s_id>')

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<u_id>')

api.add_resource(Category, '/categories/<category_id>')
api.add_resource(Categories, '/categories')

auth_api.add_resource(UserRegistration, '/register')
auth_api.add_resource(UserLogin, '/login')
