import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    LOGIN_DISABLED = False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    CAPTCHA_PUBLIC_KEY = '6Ldjhd0ZAAAAAJu7X57T6Xw07WAeJofqMIoU9MR1'
    CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bookery'
    LOGIN_DISABLED = True
    CAPTCHA_PUBLIC_KEY = '6Ldqht0ZAAAAAHMkqJhphvwKDYb6ioOK_9rj6tt7'
    CAPTCHA_SECRET_KEY = '6Ldqht0ZAAAAAI2Gat1bzw8JaV22VuUBfpqtp6JP'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bookery_test'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
