# from app import db, app
from app import db, app
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    try:

        user1 = User(id=8, email='123@gmail.com', username='admin', password=generate_password_hash('1234'))
        # user2 = User(id=2, username='user', password=generate_password_hash('12345'))


        db.session.add(user1)
        # db.session.add(user2)

       
        db.session.commit()

        print("Dos usuarios han sido añadidos.")

    except Exception as e:
        print(f"Error al añadir usuarios: {e}")
