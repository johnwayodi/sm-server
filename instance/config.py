"""Configuration Modes for the Application"""
import os


class Config:
    """Default Configuration"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('API_SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class Development(Config):
    """Development Configuration"""
    DEBUG = True


class Testing(Config):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASS')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class Production(Config):
    """Production Configuration"""
    DEBUG = False


APP_CONFIG = {
    "development": Development,
    "production": Production,
    "testing": Testing
}
