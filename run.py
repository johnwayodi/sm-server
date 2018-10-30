"""Runs the Application using development configuration"""
from flasgger import Swagger

from storemanager import create_app
from flask_jwt_extended import JWTManager

app = create_app("development")

jwt = JWTManager(app)
swagger = Swagger(app)

if __name__ == '__main__':
    app.run()
