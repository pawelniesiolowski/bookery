import logging


logger = logging.getLogger()


def setup_logger(app):
    formatter = logging.Formatter(
        '[%(asctime)s] - %(pathname)s:%(lineno)d - %(levelname)s: %(message)s',
        '%d-%m %H:%M:%S'
    )

    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(app.config['LOG_LEVEL'])
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
