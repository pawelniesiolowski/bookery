"""Report module"""


from flask import Blueprint


report = Blueprint('report', __name__, template_folder='templates')


# pylint: disable=wrong-import-position, cyclic-import

from . import controllers  # noqa

# pylint: enable=wrong-import-position, cyclic-import
