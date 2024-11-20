# Importación de las librerías necesarias para el proyecto
from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
import pytz
import secrets
import string
from datetime import datetime
from forms import LoginForm, ForgotPasswordForm, ResetPasswordForm
from models import db, User, Denuncia


# Creación de la instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denuncias.db'  # Ruta de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilitar el seguimiento de modificaciones
app.config['SECRET_KEY'] = 'secreto1234'  # Clave secreta para las sesiones de Flask

# Inicialización de la base de datos con la app
db.init_app(app)

# Inicialización de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Vista de login por defecto cuando no hay sesión activa

# Función de carga del usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creación de las tablas de la base de datos si no existen
with app.app_context():
    db.create_all()

# Ruta principal de la aplicación
@app.route('/')
def index():
    form = LoginForm()  # Instanciación del formulario de login
    return render_template('index.html', form=form)

# Ruta de login, maneja los métodos GET y POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtención de los datos del formulario de login
        username = request.form['username']
        password = request.form['password']
        
        # Búsqueda del usuario en la base de datos por nombre de usuario
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Comprobación de la contraseña
            login_user(user)  # Iniciar sesión para el usuario
            return redirect(url_for('admin_dashboard'))  # Redirigir al dashboard del admin
        else:
            flash('Usuario o contraseña incorrecta', 'danger')  # Mensaje de error
            return redirect(url_for('login'))  # Redirigir a la página de login

    return render_template('login.html')

# Ruta para la recuperación de contraseña
@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPasswordForm()  # Instanciación del formulario de recuperación de contraseña

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:  # Si el usuario existe, redirigir a la vista de reset de contraseña
            return redirect(url_for('resetPassword', email=user.email))
        else:  # Si no existe el usuario, mostrar mensaje de error
            flash('El correo electrónico no se encuentra registrado', 'danger')

    return render_template('ForgotPassword.html', form=form)

# Ruta para el reseteo de contraseña
@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    email = request.args.get('email')  # Obtención del correo del usuario desde la URL
    user = User.query.filter_by(email=email).first()
    form = ResetPasswordForm()

    if form.validate_on_submit():  # Si el formulario es válido, se actualiza la contraseña
        user.set_password(form.password.data)
        db.session.commit()  # Guardar los cambios en la base de datos
        flash('Tu contraseña ha sido actualizada', 'success')  # Mensaje de éxito
        return redirect(url_for('resetPassword', email=email))  # Redirigir a la misma página

    return render_template('ResetPassword.html', form=form)

# Ruta para el dashboard del administrador (requiere estar logueado)
@app.route('/admin_dashboard')
@login_required  # El acceso está restringido solo a usuarios logueados
def admin_dashboard():
    denuncias = Denuncia.query.all()  # Obtener todas las denuncias de la base de datos
    response = make_response(render_template('admin_dashboard.html', denuncias=denuncias))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'  # No almacenar en caché
    response.headers['Pragma'] = 'no-cache'  # Deshabilitar caché
    return response

# Ruta para la vista del formulario de denuncia
@app.route('/denunciaForm')
def denunciaForm():
    return render_template('denunciaForm.html')

# Ruta para la sección "Quienes Somos"
@app.route('/quienesSomos')
def quienesSomos():
    return render_template('quienesSomos.html')

# Ruta para la creación de una nueva denuncia
@app.route('/denuncia', methods=['GET', 'POST'])
def denunciar():
    colombia_tz = pytz.timezone('America/Bogota')  # Establecer la zona horaria de Colombia

    if request.method == 'POST':
        # Obtención de los datos del formulario de denuncia
        fecha = request.form['fecha']
        motivo = request.form['motivo']
        pais = request.form['pais']
        entidad = request.form['entidad']
        redaccion = request.form['redaccion']
        fecha_actual = datetime.now(colombia_tz)  # Fecha y hora actual en la zona horaria de Colombia

        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')  # Intentar convertir la fecha proporcionada
        except ValueError:
            flash("Formato de fecha inválido. Por favor ingrese una fecha válida.", 'danger')  # Error si el formato es incorrecto
            return redirect(url_for('denunciar'))  # Volver al formulario de denuncia

        # Crear una nueva denuncia con los datos proporcionados
        nueva_denuncia = Denuncia(denuncia=redaccion, fechaRegistro=fecha_actual, fecha=fecha, motivo=motivo, pais=pais, entidad=entidad)
        db.session.add(nueva_denuncia)  # Añadir la denuncia a la base de datos
        db.session.commit()  # Guardar los cambios
        flash('Denuncia radicada con éxito', 'success')  # Mensaje de éxito
        return redirect(url_for('denunciar'))  # Redirigir de vuelta al formulario de denuncia

    denuncias = Denuncia.query.all()  # Obtener todas las denuncias de la base de datos
    return render_template('denunciar.html', denuncias=denuncias)

# Ruta para eliminar una denuncia (requiere estar logueado)
@app.route('/delete_denuncia/<int:id>/<action>', methods=['POST'])
@login_required
def delete_denuncia(id, action):
    denuncia = Denuncia.query.get_or_404(id)  # Buscar la denuncia por ID

    if action == 'eliminar':
        # Eliminar la denuncia de la base de datos
        db.session.delete(denuncia)
        db.session.commit()  # Guardar los cambios
        flash('Denuncia eliminada con éxito', 'success')
    elif action == 'enviar':
        # Lógica para "enviar a la fiscalía" (sin eliminar la denuncia)
        # En este caso solo mostramos un mensaje sin necesidad de modificar la base de datos
        flash('Denuncia enviada a la fiscalía con éxito', 'success')

    return redirect(url_for('admin_dashboard'))  # Redirigir al dashboard del admin

@app.route('/send_to_fiscalia/<int:id>', methods=['POST'])
def send_to_fiscalia(id):
    # Lógica para enviar la denuncia a la fiscalía
    flash('Denuncia enviada a la fiscalía.')
    return redirect(url_for('admin_dashboard'))

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cerrar sesión
    return redirect(url_for('index'))  # Redirigir a la página de inicio

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
