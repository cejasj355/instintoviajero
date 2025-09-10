from app import app
from extensions import db
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash


with app.app_context():
    admin = Usuario.query.filter_by(username="diego_admin").first()
    if not admin:
        admin = Usuario(
            username="diego_admin",
            password=generate_password_hash("nanfifruti128"),  # cambiá la contraseña por una segura
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado correctamente.")
    else:
        print("⚠️ Ya existe un usuario administrador.")