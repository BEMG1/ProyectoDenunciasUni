from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    sumbit = SubmitField('Enviar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('nueva contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmas nueva contraseña', validators=[DataRequired(), EqualTo('password')])
    sumbit = SubmitField('Restablecer contraseña')