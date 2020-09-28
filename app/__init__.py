from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .catalog import catalog as catalog_blueprint
    app.register_blueprint(catalog_blueprint)

    from .receiver import receiver as receiver_blueprint
    app.register_blueprint(receiver_blueprint)

    return app
