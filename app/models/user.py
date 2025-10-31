from .. import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    company = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    metrics = db.relationship('Metrics', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'