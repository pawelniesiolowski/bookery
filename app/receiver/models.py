"""Database models"""


from typing import Dict
from datetime import datetime
from sqlalchemy.orm import validates
from flask_sqlalchemy.model import DefaultMeta
from .. import db

BaseModel: DefaultMeta = db.Model


class Receiver(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(55), nullable=False)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, name: str, surname: str) -> None:
        self.name = name
        self.surname = surname

    # pylint: disable=unused-argument,no-self-use

    @validates('name')
    def validate_name(self, key: str, value: str) -> str:
        assert value and isinstance(value, str)\
            and len(value) > 1 and len(value) < 26
        return value

    @validates('surname')
    def validate_surname(self, key: str, value: str) -> str:
        assert value and isinstance(value, str)\
            and len(value) > 1 and len(value) < 56
        return value

    # pylint: enable=unused-argument,no-self-use

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        self.deleted_at = datetime.now()

    def format(self) -> Dict:
        return {
            'id': self.id,
            'name': f'{self.name} {self.surname}'
            }

    def __repr__(self) -> str:
        return f'''
<Receiver
    id: {self.id},
    name: {self.name},
    surname: {self.surname},
    deleted_at: {self.deleted_at}
>'''
