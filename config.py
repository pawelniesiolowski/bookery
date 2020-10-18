import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    LOGIN_DISABLED = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bookery'
    LOGIN_DISABLED = True


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bookery_test'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
