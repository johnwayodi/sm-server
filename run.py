"""Runs the Application using development configuration"""
from flasgger import Swagger

from storemanager import create_app
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from storemanager.api.v2.database.database import Database, execute_query
from storemanager.api.v2.utils.custom_checks import is_token_revoked

app = create_app("development")
Database.drop_tables()
Database.create_all_tables()
jwt = JWTManager(app)
CORS(app)

template = {
    "swagger": "3.0",
    "info": {
        "title": "Store Manager API",
        "description": "API for the store manager application, with PostgreSQL database",
        "version": "2.0.0"
    }
}

swagger = Swagger(app, template=template)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return is_token_revoked(jti)


if __name__ == '__main__':
    app.run()
