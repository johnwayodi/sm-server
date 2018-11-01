"""
Module containing function create_app() which when called creates a new app
"""
import os
from flask import Flask
from instance.config import APP_CONFIG
from storemanager.api.v2 import api_blueprint, auth_blueprint


def create_app(config_name):
    """Create app and register api"""
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')
    app.config['SWAGGER'] = {'title': 'Store Manager API', 'uiversion': 3}
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)
    return app
