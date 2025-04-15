from run import app
from app import db
from app.models import User

# Establece el contexto de la aplicación
with app.app_context():
    # Crea un nuevo usuario
    nuevo_usuario = User(
        username='admin',
        email='admin@cutonala.mx'
    )

    # Asigna la contraseña hasheada
    nuevo_usuario.set_password('Pass123')

    # Agrega el usuario a la base de datos y guarda los cambios
    db.session.add(nuevo_usuario)
    db.session.commit()
