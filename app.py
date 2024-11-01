from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
import pytz
from datetime import datetime
from forms import LoginForm, ForgotPasswordForm, ResetPasswordForm
from models import db, User, Denuncia


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denuncias.db'  # Ajusta la ruta según tu estructura
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secreto1234'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form = form)

# @app.route('/forgotPassword')
# def forgotPassword():
#     form = ForgotPasswordForm()
#     if form.validate_on_sumbit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             token = user.get_reset_password_token()
#             send_reset_email(user, token)
#             flash('Un correo con instrucciones para restablecer la contraseña ha sido enviado.', 'info')
#             return redirect(url_for('login'))
#     return render_template('ForgotPassword.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
            return redirect(url_for('login')) 

    return render_template('login.html')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    denuncias = Denuncia.query.all()
    response = make_response(render_template('admin_dashboard.html', denuncias=denuncias))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/denunciar', methods=['GET', 'POST'])
def denunciar():

    colombia_tz = pytz.timezone('America/Bogota')

    if request.method == 'POST':
        denuncia_contenido  = request.form['denuncia']
        fecha_actual = datetime.now(colombia_tz)
        nueva_denuncia = Denuncia(denuncia=denuncia_contenido, fecha = fecha_actual)
        db.session.add(nueva_denuncia)
        db.session.commit()
        flash('Denuncia radicada con exito', 'success')
        return redirect(url_for('denunciar'))

    denuncias = Denuncia.query.all()
    return render_template('denunciar.html', denuncias = denuncias)

@app.route('/delete_denuncia/<int:id>', methods=['POST'])
@login_required
def delete_denuncia(id):
    denuncia = Denuncia.query.get_or_404(id)
    db.session.delete(denuncia)
    db.session.commit()
    flash('Denuncia eleminada con exito', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
