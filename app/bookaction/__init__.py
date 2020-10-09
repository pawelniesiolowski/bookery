from flask import Blueprint

bookaction = Blueprint('bookaction', __name__)

from . import controllers  # noqa
