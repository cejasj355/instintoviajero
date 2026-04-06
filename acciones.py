from flask import Blueprint, render_template, request, url_for, redirect, g, session, flash, current_app, Response, abort
from werkzeug.utils import secure_filename
from extensions import db
import os
import uuid
from slugify import slugify
from PIL import Image
from models import Blog, SalidaTrekking
from functools import wraps

from models import SalidaTrekking, Usuario
bp = Blueprint('acciones', __name__, url_prefix='/acciones')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificamos si el usuario está logueado y si es admin
        if not session.get('is_admin'):
            return abort(403) # Error de "Prohibido"
        return f(*args, **kwargs)
    return decorated_function

#RUTA HACIA LA PAGINA NOSOTROS
@bp.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@bp.route('/log')
def pag_log():
    return render_template('/auth/login.html')

@bp.route('/ver-salida/<slug>')
def ver_salida(slug):
    salida = SalidaTrekking.query.filter_by(slug=slug).first_or_404()
    return render_template('ver_salida.html', salida=salida)


@bp.route('/proximas_salidas')
def proximas_salidas():
    salidas = SalidaTrekking.query.all()
    return render_template('proximas_salidas.html', salidas=salidas)

@bp.route('/ver_blogs/<int:id>')
def ver_blogs(id):
    blogs_total = Blog.query.filter_by(id=id).first_or_404()
    return render_template('ver_blog.html', blogs_total=blogs_total)

@bp.route('/mostrar_blogs', methods=['GET', 'POST'])
def mostrar_blogs():
    blogs_total = Blog.query.all()
    return render_template('blogs.html', blogs_total = blogs_total)