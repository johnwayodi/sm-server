"""Runs the Application using development configuration"""
from flasgger import Swagger

from storemanager import create_app
from flask_jwt_extended import JWTManager
from storemanager.api.v2.database.database import Database

app = create_app("development")
Database.drop_tables()
Database.create_all_tables()
jwt = JWTManager(app)

template = {
    "swagger": "3.0",
    "info": {
        "title": "Store Manager API",
        "description": "API for the store manager application, with PostgreSQL database",
        "version": "2.0.0"
    }
}

swagger = Swagger(app, template=template)

if __name__ == '__main__':
    app.run()
