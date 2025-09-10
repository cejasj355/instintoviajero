from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from models import Usuario
from extensions import db


app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY='instinto-trekking',
    SQLALCHEMY_DATABASE_URI='sqlite:///../instance/datos.db',
)
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente.")


# # Registrar Blueprints
import acciones, auth
app.register_blueprint(acciones.bp)
app.register_blueprint(auth.bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proximas_salidas')
def proximas_salidas():
    return render_template('proximas_salidas.html')

@app.route('/ascenso-cerro-champaqui-cordoba')
def cerro_champaqui():
    return render_template('/salidas/cerro_champaqui.html')

@app.route('/trekking-uritorco-nocturno-amanecer-en-cumbre')
def uritorco():
    return render_template('/salidas/uritorco.html')


@app.route('/excursion-trekking-gigantes')
def gigantes_full():
    return render_template('/salidas/gigantes_full.html')

@app.route('/vallecitos-mendoza-ascenso-cerro-adolfo-calle-y-cerro-stepanek')
def vallecitos():
    return render_template('/salidas/vallecitos.html')

@app.route('/ascenso-cerro-penitentes-mendoza')
def cerro_penitentes():
    return render_template('/salidas/cerro_penitentes.html')

#RUTA HACIA LA PAGINA NOSOTROS
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/log')
def login():
    return render_template('auth/login.html')


if __name__ == '__main__':
    app.run(debug = True)
    