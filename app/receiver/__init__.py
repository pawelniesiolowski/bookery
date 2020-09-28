from flask import Blueprint

receiver = Blueprint('receiver', __name__, template_folder='templates')

from . import controllers  # noqa
