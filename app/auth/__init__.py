from flask import Blueprint
from flask_login import LoginManager
from .models import User

auth = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Zaloguj się'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from . import controllers  # noqa
