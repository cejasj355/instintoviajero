from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from models import SalidaTrekking, Usuario
from extensions import db
from flask_ckeditor import CKEditor
import os


app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY='instinto-trekking',
    SQLALCHEMY_DATABASE_URI='sqlite:///../instance/datos.db',
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ckeditor = CKEditor(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente.")


# # Registrar Blueprints
import acciones, auth, admin
app.register_blueprint(acciones.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)

@app.route('/')
def index():
    salida = SalidaTrekking.query.all()
    return render_template('index.html', salida=salida)


if __name__ == '__main__':
    app.run(debug = True)
    