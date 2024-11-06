
# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class Denuncia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denuncia = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
