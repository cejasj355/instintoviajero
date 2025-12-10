from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class SalidaTrekking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_salida = db.Column(db.String(255))
    foto_carta = db.Column(db.String(255))
    foto_portada = db.Column(db.String(255))
    titulo = db.Column(db.String(100))
    subtitulo = db.Column(db.String(150))
    dias = db.Column(db.String(50))
    contado = db.Column(db.String(50))
    lugarsalida = db.Column(db.String(100))
    dificultad = db.Column(db.String(50))
    recorrido = db.Column(db.Text)
    encuentro = db.Column(db.String(100))
    inicio = db.Column(db.String(100))
    fin = db.Column(db.String(100))
    edad = db.Column(db.String(50))
    proximasfechas = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    trescuotas = db.Column(db.String(50))
    seiscuotas = db.Column(db.String(50))
    finpromo = db.Column(db.String(100))
    incluye = db.Column(db.Text)
    opcional = db.Column(db.Text)
    itinerario = db.Column(db.Text)
    equipamiento = db.Column(db.Text)
    preguntas = db.Column(db.Text)
    foto_uno = db.Column(db.String(255))
    foto_dos = db.Column(db.String(255))
    foto_tres = db.Column(db.String(255))
    codigo = db.Column(db.Text)