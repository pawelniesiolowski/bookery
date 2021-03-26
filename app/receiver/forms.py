"""Forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ReceiverForm(FlaskForm):
    name = StringField('Imię:', validators=[
        DataRequired(message="Imię jest wymagane"),
        Length(
            min=2,
            max=25,
            message='Imię musi mieć od 2 do 25 znaków'
            )
        ])
    surname = StringField(
        'Nazwisko:', validators=[
            DataRequired(message="Nazwisko jest wymagane"),
            Length(
                min=2,
                max=55,
                message='Nazwisko musi mieć od 2 do 55 znaków'
                )
            ])
    submit = SubmitField('Zapisz')
