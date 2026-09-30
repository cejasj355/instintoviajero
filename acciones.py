import email

from flask import Blueprint, render_template, request, url_for, redirect, g, session, flash, current_app, Response, abort
from werkzeug.utils import secure_filename
from extensions import db, mail
from slugify import slugify
from PIL import Image
import os
from models import Blog, FichaMedica, SalidaTrekking
from functools import wraps
from models import SalidaTrekking, Usuario
from models import FichaMedica
from flask_mail import Message

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

@bp.route('/formulario', methods=['GET'])
def formulario():
    return render_template('formulario.html')

@bp.route('/enviar-formulario/', methods=['POST'])
def enviar_formulario():
    datos = request.form.to_dict()

    lista_patologias = request.form.getlist('patologias')
    datos['patologias'] = ', '.join(lista_patologias) if lista_patologias else 'Ninguna Seleccionada'
    
    email_usuario = datos.get('email')
    nombre_usuario = datos.get('nombreCompleto', 'Trekker')

    try:
        # 1. Guardar en Base de Datos
        nueva_ficha = FichaMedica(
            nombre=nombre_usuario,
            email=datos.get('email', 'Sin Email'),
            dni=datos.get('dniPasaporte', 'Sin DNI'),
            expedicion=datos.get('expedicionDestino', 'Sin Expedición'),
            datos_formulario=datos
        )
        db.session.add(nueva_ficha)
        db.session.commit()

        # 2. Enviar Emails dentro de una ÚNICA conexión SMTP
        correo_admin = os.getenv('MAIL_ADMIN_RECIPIENT')
        
        with mail.connect() as conn:
            # Email al Administrador
            if correo_admin:
                msg_admin = Message(
                    subject=f"Nueva Ficha Médica: {nombre_usuario}",
                    recipients=[correo_admin] 
                )
                
                cuerpo_email = (
                    f"¡Se ha recibido una nueva Ficha Médica de Inscripción!\n\n"
                    f"DATOS PRINCIPALES:\n"
                    f"- Nombre: {nombre_usuario}\n"
                    f"- Email: {email_usuario}\n"
                    f"- DNI/Pasaporte: {datos.get('dniPasaporte')}\n"
                    f"- Expedición: {datos.get('expedicionDestino')}\n"
                    f"- Patologías: {datos.get('patologias')}\n\n"
                    f"TODOS LOS DATOS ENVIADOS:\n"
                )
                for clave, valor in datos.items():
                    cuerpo_email += f"\n* {clave}: {valor}"

                msg_admin.body = cuerpo_email
                conn.send(msg_admin)

            # Email de confirmación al Usuario
            if email_usuario:
                msg_usuario = Message(
                    subject="Confirmación de Ficha Médica - Instinto Trekking",
                    recipients=[email_usuario]
                )
                msg_usuario.body = (
                    f"Hola {nombre_usuario},\n\n"
                    f"Hemos recibido correctamente tu Ficha Médica de Inscripción para {datos.get('expedicionDestino', 'la expedición')}.\n\n"
                    f"¡Nos vemos pronto en la montaña!\n"
                    f"El equipo de Instinto Viajero."
                )
                conn.send(msg_usuario)

        flash("¡Tu Ficha Médica de Inscripción se guardó y envió con éxito!", "success")
        return redirect(url_for('acciones.formulario'))

    except Exception as e:
        db.session.rollback()
        # Esto imprimirá el error real en tu log de PythonAnywhere (stderr log)
        import traceback
        print(f"Error detallado al enviar/guardar la ficha:\n{traceback.format_exc()}")
        
        flash("Ocurrió un error al guardar la ficha médica.", "danger")
        return redirect(url_for('acciones.formulario'))