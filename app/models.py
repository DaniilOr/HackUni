from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    priority = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    distance = db.Column(db.Float)
    role = db.Column(db.Text)
    rating = db.Column(db.Float)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, name, email, priority=False, price=1000, distance=1000, role='', description=''):
        self.username = name
        self.email = email
        self.priority = priority
        self.price = price
        self.distance = distance
        self.role = role
        self.description = description
        self.rating = 0.0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
