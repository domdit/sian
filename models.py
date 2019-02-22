from siamsite import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.Text)
    rank = db.Column(db.Integer)
    head = db.Column(db.Boolean, default=False)
    spice = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"MenuItems('{self.name}', '{self.description}')"



