from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
import pyotp

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    last_ip_address = db.Column(db.String(45))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False, default=pyotp.random_base32())
    otp_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username
