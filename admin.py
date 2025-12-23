from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import SalidaTrekking
from app import db
import app
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')
@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')



import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename

def guardar_imagen(file, calidad=85):
    if not file or file.filename == '':
        return None

    # Crear carpeta si no existe
    upload_folder = os.path.join('static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # Nombre único
    filename = f"{uuid.uuid4().hex}.webp"
    filepath = os.path.join(upload_folder, filename)

    # Abrir imagen
    img = Image.open(file)

    # Convertir si viene con transparencia
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Guardar en WEBP
    img.save(filepath, "WEBP", quality=calidad, method=6)

    return filename


# def guardar_imagen(file):
#     if file:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join('static', 'uploads', filename)
#         file.save(filepath)
#         return filename
#     return None

@bp.route('/crear-post', methods=['GET', 'POST'])
def crear_post():
    if request.method == 'POST':
        nueva_salida = SalidaTrekking(
            tipo_salida=request.form['tipo-salida'],
            titulo=request.form['titulo'],
            subtitulo=request.form['subtitulo'],
            dias=request.form['dias-noches'],
            contado=request.form['precio-contado'],
            lugarsalida=request.form['lugar-salida'],
            dificultad=request.form['dificultad'],
            recorrido=request.form['recorrido'],
            encuentro=request.form['encuentro'],
            inicio=request.form['inicio'],
            fin=request.form['fin'],
            edad=request.form['edad'],
            proximasfechas=request.form['proximas-fechas'],
            descripcion=request.form['descripcion-salida'],
            trescuotas=request.form['tres-cuotas'],
            seiscuotas=request.form['seis-cuotas'],
            finpromo=request.form['fin-promo'],
            incluye=request.form['incluye'],
            opcional=request.form['opcional'],
            itinerario=request.form['itinerario'],
            equipamiento=request.form['equipamiento'],
            preguntas=request.form['preguntas'],
            codigo = request.form['codigo']
        )
        foto_carta = request.files.get('foto-carta')
        if foto_carta:
            ruta_foto_carta = guardar_imagen(foto_carta)
            nueva_salida.foto_carta = ruta_foto_carta
        
        foto_portada = request.files.get('foto-portada')
        if foto_portada:
            ruta_foto_portada = guardar_imagen(foto_portada)
            nueva_salida.foto_portada = ruta_foto_portada
        
        foto_uno = request.files.get('foto-uno')
        if foto_uno:
            ruta_foto_uno = guardar_imagen(foto_uno)
            nueva_salida.foto_uno = ruta_foto_uno
        
        foto_dos = request.files.get('foto-dos')
        if foto_dos:
            ruta_foto_dos = guardar_imagen(foto_dos)
            nueva_salida.foto_dos = ruta_foto_dos
        
        foto_tres = request.files.get('foto-tres')
        if foto_tres:
            ruta_foto_tres = guardar_imagen(foto_tres)
            nueva_salida.foto_tres = ruta_foto_tres
        
        
        
            
        db.session.add(nueva_salida)
        db.session.commit()

    return redirect(url_for('acciones.lista_salidas')) 

    # ✅ Si entra por GET, renderiza el formulario
    return render_template('admin/crear_post.html')

        