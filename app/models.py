from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from geoalchemy2 import Geometry
from enum import Enum
from sqlalchemy import Enum as SQLEnum


from flask_login import UserMixin

class admin_users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return admin_users.query.get(int(user_id))


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    cars = db.relationship('Car', back_populates='owner', lazy=True)

class Car(db.Model):
    __tablename__ = 'user_cars'

    car_id = db.Column(db.String(80), primary_key=True)
    car_plates = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    owner = db.relationship('User', back_populates='cars')


class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.spot_id'), nullable=False)  # ForeignKey apuntando a ParkingSpot
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(1), nullable=False)
    user_car_id = db.Column(db.Integer)

    # Relación con la tabla 'users' (ya la tienes configurada correctamente)
    user = db.relationship('User', backref='reservations', lazy=True)

    # Relación con la tabla 'parking_spots', cambiando el backref para evitar conflicto
    spot = db.relationship('ParkingSpot', backref='spot_reservations', lazy=True)

    def __repr__(self):
        return f"<Reservation {self.reservation_id} - User {self.user_id}, Spot {self.spot_id}>"


class StatusEnum(Enum):
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    OCCUPIED = 'occupied'

    def __str__(self):
        return self.value

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    spot_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.AVAILABLE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(Geometry('POINT'))
    section = db.Column(db.String(3), default='default_section')

   
    reservations = db.relationship('Reservation', backref='reservations_spots', lazy=True)

    def __repr__(self):
        return f"<ParkingSpot {self.spot_id} - {self.status}>"
