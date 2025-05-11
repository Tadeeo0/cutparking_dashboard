from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import admin_users
from app.models import User
from app.models import Reservation
from sqlalchemy import text
from app.models import ParkingSpot
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('main', __name__)

#login
@bp.route('/')
def home():
    return redirect(url_for('main.login'))

#inicio de sesion
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       
        user = admin_users.query.filter_by(email=form.email.data).first()
        if user:
            
            if user.is_active:
                if user.check_password(form.password.data):
                    login_user(user)
                   
                    return redirect(url_for('main.dashboard'))  
                else:
                    flash('Correo electrónico o contraseña incorrectos.')
            else:
                flash('Tu cuenta está inactiva. Por favor, contacta al administrador.')
        else:
            flash('Correo electrónico o contraseña incorrectos.')
    return render_template('login.html', form=form)


#registro
@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.email != 'admin@cutonala.mx':  
        flash('No tienes permisos para registrar usuarios.')
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = admin_users(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado correctamente.')
        return redirect(url_for('main.dashboard'))
    return render_template('register.html', form=form)

#principal
@bp.route('/dashboard')
@login_required
def dashboard():
    #Contar el numero de usuarios
    num_users = db.session.execute(text("SELECT COUNT(*) FROM users"))
    total_users = num_users.scalar()  

    num_cars = db.session.execute(text("SELECT COUNT(*) FROM user_cars"))
    total_cars = num_cars.scalar()

    num_spots = db.session.execute(text("SELECT COUNT(*) FROM parking_spots"))
    total_spots = num_spots.scalar()

    spots_available = db.session.execute(text("SELECT COUNT(*) FROM parking_spots where status = 'available'"))
    total_spots_available = spots_available.scalar()

    spots_reserved = db.session.execute(text("SELECT COUNT(*) FROM parking_spots where status = 'reserved'"))
    total_spots_reserved = spots_reserved.scalar()

    spots_occupied = db.session.execute(text("SELECT COUNT(*) FROM parking_spots where status = 'occupied'"))
    total_spots_ccupied = spots_occupied.scalar()

    return render_template('dashboard.html', user=current_user, total_users=total_users, total_cars = total_cars, total_spots = total_spots, 
                           total_spots_available = total_spots_available, total_spots_reserved = total_spots_reserved, 
                           total_spots_ccupied= total_spots_ccupied)

#Cerrar Sesion
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# usuarios
@bp.route('/users')
@login_required
def users():
    users_list = User.query.all()
    
    return render_template('users_list.html', users=users_list)

# reservas
@bp.route('/view_reservations', methods=['GET'])
@login_required
def view_reservations():
    reservations = Reservation.query.all()  # Obtener todas las reservas
    return render_template('view_reservations.html', reservations=reservations)

#spots
@bp.route('/view_spots', methods=['GET'])
@login_required
def view_spots():
    spots = db.session.query(
        ParkingSpot.spot_id,
        ParkingSpot.status,
        ParkingSpot.created_at,
        ParkingSpot.section,
        func.ST_X(ParkingSpot.location).label("lat"),
        func.ST_Y(ParkingSpot.location).label("lng")
    ).all()  
    
    return render_template('view_spots.html', spots=spots)

#añadir spot
@bp.route('/add_spot', methods=['GET', 'POST'])
@login_required
def add_spot():
    if request.method == 'POST':
        # Obtener datos del formulario
        status = request.form.get('status')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        section = request.form.get('section')

        # Verificar si latitud y longitud no son vacíos
        if not latitude or not longitude:
            flash('Por favor ingrese ambos, latitud y longitud.', 'error')
            return redirect(url_for('main.add_spot'))

        # Crear la ubicación en formato POINT
        location = f"POINT({latitude} {longitude})"
        created_at = datetime.utcnow()

        # Crear un nuevo espacio de estacionamiento
        new_spot = ParkingSpot(status=status, location=location, created_at=created_at, section = section)
        db.session.add(new_spot)
        db.session.commit()

        flash('Nuevo espacio de estacionamiento agregado correctamente.')
        return redirect(url_for('main.view_spots'))

    return render_template('add_spot.html')



#eliminar spot
@bp.route('/delete_spot/<int:spot_id>', methods=['GET'])
@login_required
def delete_spot(spot_id):
    # Buscar el espacio en la base de datos
    spot = ParkingSpot.query.get(spot_id)
    if spot:
        # Eliminar el espacio de estacionamiento
        db.session.delete(spot)
        db.session.commit()
        flash('Espacio de estacionamiento eliminado correctamente.')
    else:
        flash('El espacio de estacionamiento no existe.')

    return redirect(url_for('main.view_spots'))
