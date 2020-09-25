from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    NumberRange
)
from .isbn_validator import ISBNValidator


class BookForm(FlaskForm):
    title = StringField('Tytuł:', validators=[
        DataRequired(message="Tytuł jest wymagany"),
        Length(
            min=2,
            max=255,
            message='Tytuł książki musi mieć od 2 do 255 znaków'
        )
    ])
    authors = StringField(
        'Autor:',
        filters=[lambda authors: authors or None],
        validators=[
            Optional(),
            Length(
                min=2,
                max=255,
                message='Autor książki musi mieć od 2 do 255 znaków'
            )
        ]
    )
    isbn = StringField(
        'ISBN:',
        filters=[lambda isbn: isbn or None],
        validators=[
            Optional(),
            Regexp(
                ISBNValidator.regex,
                message='ISBN musi się składać z 11 lub 13 cyfr'
            )
        ]
    )
    price = DecimalField(
        'Cena:',
        validators=[
            Optional(),
            NumberRange(
                min=0,
                max=99999.99,
                message='Cena musi być w wysokości od 0 do 99999.99 zł'
            )
        ]
    )
    submit = SubmitField('Zapisz')
