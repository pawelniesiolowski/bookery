from .. import db
from sqlalchemy.orm import validates
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'''
<User
    id: {self.id},
    email: {self.email}
>'''
