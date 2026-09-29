from dotenv import load_dotenv
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from models import SalidaTrekking, Usuario
from extensions import db, migrate
from flask_ckeditor import CKEditor
import os
import acciones, auth, admin
from extensions import mail


load_dotenv()
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-por-defecto-dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///../instance/datos.db')

# Configuración de Flask-Mail leyendo de entorno
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

ckeditor = CKEditor(app)
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

with app.app_context():
    db.create_all()


# # Registrar Blueprints
app.register_blueprint(acciones.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)

@app.route('/')
def index():
    salida = SalidaTrekking.query.all()
    return render_template('index.html', salida=salida)


if __name__ == '__main__':
    app.run(debug = True)
    