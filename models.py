
# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.string(150), nulleable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Denuncia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denuncia = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
