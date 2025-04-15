from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Verifica si el usuario está activo
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



@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.email != 'admin@cutonala.mx':  
        flash('No tienes permisos para registrar usuarios.')
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado correctamente.')
        return redirect(url_for('main.dashboard'))
    return render_template('register.html', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

