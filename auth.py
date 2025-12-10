from flask import Blueprint, render_template, request, session, url_for, redirect, g, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import Usuario
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registro', methods= ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario(username, generate_password_hash(password))
        user_name = Usuario.query.filter_by(username = username).first() #filter_by busca en la db el valor que nosotros le pasemos
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index')) #registra nuevo usuario
    return render_template('index.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        error = None
        user = Usuario.query.filter_by(username=username).first()

        if user == None:
            error = 'Nombre de usuario o contraseña incorrecto'
        elif not check_password_hash(user.password, password):          # Esto es una mala practica porque te indica el error que cometes 
            error = 'Nombre de usuario o contraseña incorrecto'
        session.clear()
        flash(error)

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin

            if user.is_admin:
                return redirect(url_for('index'))
            else:
                return redirect(url_for('acciones.index'))

        
    return redirect(url_for('acciones.pag_log'))
