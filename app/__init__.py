"""App"""


from flask import Flask, logging
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import config, ConfigName
from .logger import setup_logger


db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['NAME'] == ConfigName.PRODUCTION:
        # pylint: disable=no-member
        app.logger.removeHandler(logging.default_handler)
        # pylint: enable=no-member
        setup_logger(app)

    db.init_app(app)

    # pylint: disable=import-outside-toplevel, cyclic-import

    from .catalog import catalog as catalog_blueprint
    app.register_blueprint(catalog_blueprint)

    from .receiver import receiver as receiver_blueprint
    app.register_blueprint(receiver_blueprint)

    from .bookaction import bookaction as bookaction_blueprint
    app.register_blueprint(bookaction_blueprint)

    from .auth import auth as auth_blueprint, login_manager
    app.register_blueprint(auth_blueprint)
    login_manager.init_app(app)

    from .report import report as report_blueprint
    app.register_blueprint(report_blueprint)

    # pylint: enable=import-outside-toplevel, cyclic-import

    return app
