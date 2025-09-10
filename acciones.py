from flask import Blueprint, render_template, request, url_for, redirect, g, session, flash, current_app, jsonify
from werkzeug.utils import secure_filename
import os
from flask import current_app

from models import Usuario
bp = Blueprint('acciones', __name__, url_prefix='/acciones')

@bp.route('/log', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = Usuario.query.filter_by(username=username).first()
        if user is None:
            error = 'Usuario incorrecto.'
        elif not user.check_password(password):
            error = 'Contraseña incorrecta.'



        return render_template('auth/login.html')

