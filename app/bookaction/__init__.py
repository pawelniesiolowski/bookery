"""Book Action module"""


from flask import Blueprint


bookaction = Blueprint('bookaction', __name__)


# pylint: disable=wrong-import-position, cyclic-import

from . import controllers  # noqa

# pylint: enable=wrong-import-position, cyclic-import
