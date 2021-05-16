"""Forms"""


from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField


class ReportForm(FlaskForm):
    date = DateField('Data końcowa:')
    submit = SubmitField('Zapisz')
