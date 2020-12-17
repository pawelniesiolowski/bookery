from flask import Blueprint

report = Blueprint('report', __name__, template_folder='templates')

from . import controllers  # noqa
