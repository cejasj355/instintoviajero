from dotenv import load_dotenv
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from models import Blog, SalidaTrekking, Usuario
from extensions import db, migrate
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
import os
import acciones, auth, admin
from datetime import date
from flask import Response
from extensions import mail


load_dotenv()
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() in ("1", "true", "yes", "on")
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY no configurada")
app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///../instance/datos.db')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

ckeditor = CKEditor(app)
csrf = CSRFProtect(app)
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

with app.app_context():
    db.create_all()


# # Registrar Blueprints
app.register_blueprint(acciones.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)

BASE = "https://www.instintoviajero.tur.ar"

@app.route("/sitemap.xml")
def sitemap():
    hoy = date.today().isoformat()

    # Páginas fijas: (ruta, frecuencia, prioridad)
    entradas = [
        ("/", "weekly", "1.0"),
        ("/acciones/proximas_salidas", "daily", "0.9"),
        ("/acciones/mostrar_blogs", "weekly", "0.6"),
        ("/acciones/nosotros", "yearly", "0.6"),
    ]

    # Salidas: AJUSTÁ el modelo y el campo del slug
    for salida in SalidaTrekking.query.all():          
        entradas.append((f"/acciones/ver-salida/{salida.slug}", "monthly", "0.8"))

    
    for blog in Blog.query.all():
        entradas.append((f"/acciones/ver-blog/{blog.slug}", "monthly", "0.7"))

    items = "".join(
        f"<url><loc>{BASE}{ruta}</loc><lastmod>{hoy}</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        for ruta, freq, prio in entradas
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f"{items}</urlset>")
    return Response(xml, mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    txt = ("User-agent: *\n"
           "Disallow: /acciones/log\n"
           f"Sitemap: {BASE}/sitemap.xml\n")
    return Response(txt, mimetype="text/plain")

@app.route('/')
def index():
    salida = SalidaTrekking.query.all()
    return render_template('index.html', salida=salida)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
    