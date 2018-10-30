"""Configuration Modes for the Application"""


class Config(object):
    """Default Configuration"""
    pass


class Develop(Config):
    """Development Configuration"""

    def __init__(self):
        self.debug = True


class Production(Config):
    """Production Configuration"""

    def __init__(self):
        self.debug = False


APP_CONFIG = {
    "development": Develop,
    "production": Production
}
