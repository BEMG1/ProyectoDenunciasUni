# Importaciones necesarias
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime

# Instancia de SQLAlchemy, que se utilizará para interactuar con la base de datos
db = SQLAlchemy()

# Clase User, que representa la tabla 'user' en la base de datos
class User(db.Model, UserMixin):
    # Definición de las columnas de la tabla 'user'
    id = db.Column(db.Integer, primary_key=True)  # Columna para el ID, que es clave primaria
    email = db.Column(db.String(150), nullable=False)  # Columna para el correo electrónico, no puede ser nulo
    username = db.Column(db.String(150), nullable=False, unique=True)  # Columna para el nombre de usuario, único y no nulo
    password = db.Column(db.String(150), nullable=False)  # Columna para la contraseña, no puede ser nula

    # Método para establecer la contraseña, utilizando hashing para asegurarla
    def set_password(self, password):
        self.password = generate_password_hash(password)  # Se genera un hash para la contraseña

# Clase Denuncia, que representa la tabla 'denuncia' en la base de datos
class Denuncia(db.Model):
    # Definición de las columnas de la tabla 'denuncia'
    id = db.Column(db.Integer, primary_key=True)  # Columna para el ID, que es clave primaria
    denuncia = db.Column(db.String, nullable=False)  # Columna para el texto de la denuncia, no puede ser nulo
    motivo = db.Column(db.String, nullable=False)  # Columna para el motivo de la denuncia, no puede ser nulo
    pais = db.Column(db.String, nullable=False)  # Columna para el país, no puede ser nulo
    entidad = db.Column(db.String, nullable=False)  # Columna para la entidad, no puede ser nulo
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)  # Columna para la fecha de registro, se establece por defecto la fecha actual
    fecha = db.Column(db.DateTime, nullable=False)  # Columna para la fecha de la denuncia, no puede ser nula
