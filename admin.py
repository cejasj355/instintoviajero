from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from models import Blog, SalidaTrekking
from app import db
from flask import current_app
import os
from slugify import slugify
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from acciones import admin_required
from app import *


bp = Blueprint('admin', __name__, url_prefix='/admin')
@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def guardar_foto(file, foto_actual=None):

    if not file or file.filename == '':
        return foto_actual

    extensiones_permitidas = {'jpg', 'jpeg', 'png', 'webp'}
    extension = file.filename.rsplit('.', 1)[-1].lower()

    if extension not in extensiones_permitidas:
        return foto_actual

    # borrar imagen anterior
    if foto_actual:
        ruta_vieja = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            foto_actual
        )
        if os.path.exists(ruta_vieja):
            os.remove(ruta_vieja)

    nombre = f"{uuid.uuid4().hex}.webp"
    nombre = secure_filename(nombre)

    ruta = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        nombre
    )

    img = Image.open(file)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    tamaño_max = 2650
    img.thumbnail((tamaño_max, tamaño_max), Image.LANCZOS)

    img.save(
        ruta,
        "WEBP",
        quality=90,
        optimize=True
    )

    return nombre

def guardar_imagen(file, calidad=85):
    if not file or file.filename == '':
        return None

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.webp"
    filepath = os.path.join(upload_folder, filename)

    img = Image.open(file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Redimensionar a un máximo de 1920px de ancho (Full HD)
    if img.width > 1920:
        proportion = 1920 / float(img.width)
        height = int(float(img.height) * float(proportion))
        img = img.resize((1920, height), Image.LANCZOS)

    img.save(filepath, "WEBP", quality=calidad, method=6, optimize=True)
    return filename


@bp.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files.get('upload')

    if not file:
        return jsonify({"error": {"message": "No se envió archivo"}}), 400

    # 🔥 Nombre único y limpio
    ext = file.filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"

    # 🔥 Asegurar carpeta
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    url = url_for('static', filename=f'uploads/{filename}', _external=True)

    print("Guardado en:", filepath)
    print("URL:", url)

    return jsonify({
        "url": url
    })

def borrar_imagen(nombre_imagen):
    if not nombre_imagen:
        return

    ruta = os.path.join('static', 'uploads', nombre_imagen)
    if os.path.exists(ruta):
        os.remove(ruta)

@bp.route('/crear-post', methods=['GET', 'POST'])
@admin_required
def crear_post():
    if request.method == 'POST':
        nueva_salida = SalidaTrekking(
            tipo_salida=request.form['tipo-salida'],
            prox_desc=request.form['prox-desc'],
            titulo=request.form['titulo'],
            slug = slugify(request.form['titulo']),
            subtitulo=request.form['subtitulo'],
            dias=request.form['dias-noches'],
            contado=request.form['precio-contado'],
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
            meses_proximos=request.form['meses-proximos'],
            precio_meses_proximos=request.form['precio-meses-proximos'],
            tres_cuotas_meses=request.form['precio-tres-meses'],
            seis_cuotas_meses=request.form['precio-seis-meses'],
            finpromo=request.form['fin-promo'],
            incluye=request.form['incluye'],
            opcional=request.form['opcional'],
            no_incluye=request.form['no-incluye'],
            itinerario=request.form['itinerario'],
            equipamiento=request.form['equipamiento'],
            preguntas=request.form['preguntas'],
            codigo = request.form['codigo'],
            infoextra=request.form['info-extra'],
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

    return redirect(url_for('admin.lista_salidas')) 

    # ✅ Si entra por GET, renderiza el formulario
    return render_template('admin/crear_post.html')


@bp.route('/crear-salidas')
@admin_required
def plantilla_salidas():
    return render_template('crear_salidas.html')


@bp.route('/lista-salidas')
@admin_required
def lista_salidas():
    salidas = SalidaTrekking.query.all()
    return render_template('listado_salidas.html', salidas=salidas)


@bp.route('/editar-salida/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)

    if request.method == 'POST':
        salida.tipo_salida = request.form['tipo-salida']
        salida.prox_desc = request.form['prox-desc']
        salida.titulo = request.form['titulo']
        salida.slug = slugify(salida.titulo)
        salida.subtitulo = request.form['subtitulo']
        salida.dias = request.form['dias-noches']
        salida.contado = request.form['precio-contado']
        salida.dificultad = request.form['dificultad']
        salida.recorrido = request.form['recorrido']
        salida.encuentro = request.form['encuentro']
        salida.inicio = request.form['inicio']
        salida.fin = request.form['fin']
        salida.edad = request.form['edad']
        salida.proximasfechas = request.form['proximas-fechas']
        salida.descripcion = request.form['descripcion-salida']
        salida.trescuotas = request.form['tres-cuotas']
        salida.seiscuotas = request.form['seis-cuotas']
        salida.meses_proximos = request.form['meses-proximos']
        salida.precio_meses_proximos = request.form['precio-meses-proximos']
        salida.tres_cuotas_meses = request.form['precio-tres-meses']
        salida.seis_cuotas_meses = request.form['precio-seis-meses']
        salida.finpromo = request.form['fin-promo']
        salida.incluye = request.form['incluye']
        salida.opcional = request.form['opcional']
        salida.no_incluye = request.form['no-incluye']
        salida.itinerario = request.form['itinerario']
        salida.equipamiento = request.form['equipamiento']
        salida.preguntas = request.form['preguntas']
        salida.codigo = request.form['codigo']
        salida.infoextra = request.form['info-extra']

        # ✅ IMÁGENES
        salida.foto_carta = guardar_foto(
            request.files.get('foto-carta'),
            salida.foto_carta
        )
        salida.foto_portada = guardar_foto(
            request.files.get('foto-portada'),
            salida.foto_portada
        )
        salida.foto_uno = guardar_foto(
            request.files.get('foto-uno'),
            salida.foto_uno
        )
        salida.foto_dos = guardar_foto(
            request.files.get('foto-dos'),
            salida.foto_dos
        )
        salida.foto_tres = guardar_foto(
            request.files.get('foto-tres'),
            salida.foto_tres
        )

        db.session.commit()
        return redirect(url_for('admin.lista_salidas'))

    return render_template('editar_salidas.html', salida=salida)

@bp.route('/eliminar-salida/<int:id>', methods=['POST'])
@admin_required
def eliminar_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)

    # Borrar imágenes del disco
    borrar_imagen(salida.foto_portada)
    borrar_imagen(salida.foto_carta)
    borrar_imagen(salida.foto_uno)
    borrar_imagen(salida.foto_dos)
    borrar_imagen(salida.foto_tres)

    # Borrar de la base de datos
    db.session.delete(salida)
    db.session.commit()

    return redirect(url_for('admin.lista_salidas'))




# blogs


@bp.route('/lista-blogs')
@admin_required
def lista_blogs():
    blogs_total = Blog.query.all()
    return render_template('listado_blogs.html', blogs_total = blogs_total)

@bp.route('/crear_blog', methods=['GET', 'POST'])
@admin_required
def crear_blogs():
    return render_template('crear_blog.html')

@bp.route('/crear-nuevo-blog', methods=['POST'])
@admin_required
def crear_nuevo_blog():
    foto_blog = request.files.get('hero_image')
    # Usamos la función optimizada para WebP y reescalado
    ruta_foto_final = guardar_imagen(foto_blog) if foto_blog else "default.jpg"

    nuevo_blog = Blog(
        titulo_blog = request.form.get('titulo_blog'),
        contenido_blog = request.form.get('editor_textarea'), # Ya viene optimizado por el JS
        dificultad_blog = request.form['btnradio'],
        descripcion = request.form['descripcion'],
        ubicacion_blog = request.form.get('ubicacion_blog'),
        duracion_blog = request.form.get('duracion_expedicion'),
        msnm_blog = request.form.get('msnm'),
        km_total = request.form.get('km_total'), # Asegúrate de tener estos campos en tu modelo Blog
        punto_inicio = request.form.get('punto_inicio'),
        autor = request.form.get('autor'),
        fecha = request.form.get('fecha'),
        foto_blog = ruta_foto_final
    )

    db.session.add(nuevo_blog)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@bp.route('/eliminar-blog/<int:id>', methods=['POST'])
@admin_required
def eliminar_blog(id):
    blog = Blog.query.get_or_404(id)

    # Borrar imágenes del disco
    
    borrar_imagen(blog.foto_blog)

    # Borrar de la base de datos
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('admin.lista_blogs'))

        