from flask import Blueprint, render_template, request, url_for, redirect, g, session, flash, current_app, jsonify
from werkzeug.utils import secure_filename
from extensions import db
import os
from flask import current_app

from models import SalidaTrekking, Usuario
bp = Blueprint('acciones', __name__, url_prefix='/acciones')



@bp.route('/ascenso-cerro-champaqui-cordoba')
def cerro_champaqui():
    return render_template('/salidas/cerro_champaqui.html')

@bp.route('/trekking-uritorco-nocturno-amanecer-en-cumbre')
def uritorco():
    return render_template('/salidas/uritorco.html')


@bp.route('/excursion-trekking-gigantes')
def gigantes_full():
    return render_template('/salidas/gigantes_full.html')

@bp.route('/vallecitos-mendoza-ascenso-cerro-adolfo-calle-y-cerro-stepanek')
def vallecitos():
    return render_template('/salidas/vallecitos.html')

@bp.route('/ascenso-cerro-penitentes-mendoza')
def cerro_penitentes():
    return render_template('/salidas/cerro_penitentes.html')

#RUTA HACIA LA PAGINA NOSOTROS
@bp.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@bp.route('/log')
def pag_log():
    return render_template('/auth/login.html')

@bp.route('/crear-salidas')
def plantilla_salidas():
    return render_template('crear_salidas.html')

@bp.route('/lista-salidas')
def lista_salidas():
    salidas = SalidaTrekking.query.all()
    return render_template('listado_salidas.html', salidas=salidas)


@bp.route('/editar-salida/<int:id>', methods=['GET', 'POST'])
def editar_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)

    if request.method == 'POST':
        salida.tipo_salida = request.form['tipo-salida']
        salida.titulo = request.form['titulo']
        salida.subtitulo = request.form['subtitulo']
        salida.dias = request.form['dias-noches']
        salida.contado = request.form['precio-contado']
        salida.lugarsalida = request.form['lugar-salida']
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
        salida.finpromo = request.form['fin-promo']
        salida.incluye = request.form['incluye']
        salida.opcional = request.form['opcional']
        salida.itinerario = request.form['itinerario']
        salida.equipamiento = request.form['equipamiento']
        salida.preguntas = request.form['preguntas']
        salida.codigo = request.form['codigo']

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
        return redirect(url_for('acciones.lista_salidas'))

    return render_template('editar_salidas.html', salida=salida)
def guardar_foto(file, foto_actual):
    if file and file.filename:
        nombre = secure_filename(file.filename)
        ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre)
        file.save(ruta)
        return nombre
    return foto_actual



@bp.route('/ver-salida/<int:id>')
def ver_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)
    return render_template('ver_salida.html', salida=salida)

def borrar_imagen(nombre_imagen):
    if not nombre_imagen:
        return

    ruta = os.path.join('static', 'uploads', nombre_imagen)
    if os.path.exists(ruta):
        os.remove(ruta)


@bp.route('/eliminar-salida/<int:id>', methods=['POST'])
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

    return redirect(url_for('acciones.lista_salidas'))

@bp.route('/proximas_salidas')
def proximas_salidas():
    salidas = SalidaTrekking.query.all()
    return render_template('proximas_salidas.html', salidas=salidas)

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')