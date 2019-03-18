from siamsite import db
from flask_login import UserMixin
from datetime import *


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User('{self.email}')"


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.Text)
    rank = db.Column(db.Integer)
    head = db.Column(db.Boolean, default=False)
    spice = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "MenuItem('{self.name}', '{self.description}')"


class CaterItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.Text)
    rank = db.Column(db.Integer)
    whole = db.Column(db.String(10), unique=False)
    half = db.Column(db.String(10), unique=False)
    head = db.Column(db.Boolean, default=False)
    spice = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "CaterItem('{self.name}', '{self.description}')"


class EventItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    location = db.Column(db.String(500), unique=False, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))

    def __repr__(self):
        return "EventItem('{self.name}', '{self.location}')"


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "About('{self.id}', '{self.text}')"
