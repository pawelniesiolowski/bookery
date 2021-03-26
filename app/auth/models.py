"""Database models"""


from flask_login import UserMixin
from flask_sqlalchemy.model import DefaultMeta
from .. import db


BaseModel: DefaultMeta = db.Model


class User(UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f'''
<User
    id: {self.id},
    email: {self.email}
>'''
