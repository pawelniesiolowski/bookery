"""Catalog module"""


from flask import Blueprint


catalog = Blueprint('catalog', __name__, template_folder='templates')


# pylint: disable=wrong-import-position, cyclic-import

from . import controllers  # noqa

# pylint: enable=wrong-import-position, cyclic-import
