from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .catalog import catalog as catalog_blueprint
    app.register_blueprint(catalog_blueprint)

    from .receiver import receiver as receiver_blueprint
    app.register_blueprint(receiver_blueprint)

    from .bookaction import bookaction as bookaction_blueprint
    app.register_blueprint(bookaction_blueprint)

    from .auth import auth as auth_blueprint, login_manager
    app.register_blueprint(auth_blueprint)
    login_manager.init_app(app)

    return app
