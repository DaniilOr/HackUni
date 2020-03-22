from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
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

    def __init__(self, username, email, priority=False, price=1000, distance=1000, role='', description=''):
        self.username = username
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

    @property
    def avatar(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 128)

