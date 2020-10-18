from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired


class UserForm(FlaskForm):
    email = EmailField('Email:', validators=[
        DataRequired(message='Email jest wymagany')
    ])
    password = PasswordField('Hasło:', validators=[
        DataRequired(message='Hasło jest wymagane')
    ])
    submit = SubmitField('Zaloguj się')
