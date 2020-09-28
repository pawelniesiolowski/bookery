from .. import db
from datetime import datetime
from sqlalchemy.orm import validates


class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(55), nullable=False)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    @validates('name')
    def validate_name(self, key, value):
        assert value and isinstance(value, str)\
            and len(value) > 1 and len(value) < 26
        return value

    @validates('surname')
    def validate_surname(self, key, value):
        assert value and isinstance(value, str)\
            and len(value) > 1 and len(value) < 56
        return value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.deleted_at = datetime.now()

    def __repr__(self):
        return f'''
<Receiver
    id: {self.id},
    name: {self.name},
    surname: {self.surname},
    deleted_at: {self.deleted_at}
>'''
