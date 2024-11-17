# Importación de FlaskForm desde flask_wtf y los campos y validadores necesarios de wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# Formulario para el login de usuarios
class LoginForm(FlaskForm):
    # Campo para el nombre de usuario (requiere que se ingrese un dato)
    username = StringField('Username', validators=[DataRequired()])
    # Campo para la contraseña (requiere que se ingrese un dato)
    password = PasswordField('Password', validators=[DataRequired()])
    # Campo para el botón de envío del formulario
    submit = SubmitField('Login')

# Formulario para la recuperación de contraseña (enviando un correo electrónico)
class ForgotPasswordForm(FlaskForm):
    # Campo para el correo electrónico (requiere que se ingrese un correo válido)
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Campo para el botón de envío del formulario
    submit = SubmitField('Enviar')

# Formulario para el restablecimiento de la contraseña
class ResetPasswordForm(FlaskForm):
    # Campo para la nueva contraseña (requiere que se ingrese un dato)
    password = PasswordField('nueva contraseña', validators=[DataRequired()])
    # Campo para confirmar la nueva contraseña (debe coincidir con el campo anterior)
    confirm_password = PasswordField('Confirmas nueva contraseña', validators=[DataRequired(), EqualTo('password')])
    # Campo para el botón de envío del formulario
    submit = SubmitField('Restablecer contraseña')
