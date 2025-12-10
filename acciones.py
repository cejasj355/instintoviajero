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

@bp.route('/plantillas_salidas')
def plantilla_salidas():
    return render_template('plantilla_salidas.html')

@bp.route('/lista-salidas')
def lista_salidas():
    salidas = SalidaTrekking.query.all()
    return render_template('listado_salidas.html', salidas=salidas)

@bp.route('/ver-salida/<int:id>')
def ver_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)
    return render_template('ver_salida.html', salida=salida)

@bp.route('/eliminar-salida/<int:id>', methods=['POST'])
def eliminar_salida(id):
    salida = SalidaTrekking.query.get_or_404(id)
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