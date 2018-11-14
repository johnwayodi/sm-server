"""
Module containing function create_app() which when called creates a new app
"""
from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from instance.config import APP_CONFIG

from storemanager.api.v2.database.database import DB
from storemanager.api.v2.utils.custom_checks import is_token_revoked
from storemanager.api.v2 import api_blueprint, auth_blueprint


def create_app(config_name):
    """Create app and register api"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config['SWAGGER'] = {'title': 'Store Manager API', 'uiversion': 3}
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)

    DB.create_all_tables()
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

    Swagger(app, template=template)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return is_token_revoked(jti)

    return app
